import os

import boto3
import requests

import hnpy
import util


def score_filter(s):
    return s['score'] > 42


def slack_send_new_story(url, datapath='/tmp/data.csv', nosend=False):
    if not url:
        nosend = True

    current_data = util.read_csv(datapath)
    print("Data loaded from existing db: %s" % current_data)

    newstories = hnpy.get_stories_on_topic(hnpy.PYTHON_KEYWORDS)

    for_print = []
    for s in util.write_new_stories(newstories, current_data,
                                    datapath, score_filter):

        message = {"text": "{} points: {} - {}".format(
                   s['score'], s['title'], s['url'])
                   }
        for_print.append("Sent %s to %s" % (message, url))

        if nosend:
            continue
        else:
            r = requests.post(url, json=message)
            if r.status_code != 200:
                raise Exception("Status %s - content %s" % (r, r.content))
            else:
                print("Sent %s", message)

    for msg in for_print:
        print(msg)


def lambda_handler(event, context):
    url = os.environ["SLACK_HOOK"]
    datapath = '/tmp/data.csv'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hn.pymi.vn')
    try:
        s3.Object('hn.pymi.vn', 'data.csv').load()
    except Exception as e:
        with open(datapath, 'w') as f:
            f.write()
    else:
        bucket.download_file('data.csv', datapath)

    slack_send_new_story(url, datapath)

    bucket.put_object(ACL='public-read',
                      Bucket='hn.pymi.vn',
                      Key='data.csv',
                      Body=open(datapath).read().encode(),
                      )


def test():
    url = os.environ.get("SLACK_HOOK", '')
    slack_send_new_story(url, datapath='data.csv')


if __name__ == "__main__":
    test()
