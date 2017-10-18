import logging
import os

import boto3
import requests

import hnpy
import util

logger = logging.getLogger(__name__)


def greater_42(s):
    return s['score'] > 42


def slack_send_new_story(url, datapath='/tmp/data.csv',
                         nosend=False,
                         topics=None,
                         filter_=None):
    if not url:
        nosend = True

    current_data = util.read_csv(datapath)
    print("Hook URL: %s" % url[-10:])
    print("Data loaded from existing db: %s" % current_data)

    newstories = hnpy.get_stories_on_topic(topics)

    logger.info("Filtering on topic %s", topics)

    for_print = []
    for s in util.write_new_stories(newstories, current_data,
                                    datapath, filter_):

        message = "{} points: {} - {} ({})".format(
            s['score'], s['title'], s['url'], util.get_hn_url(s['id'])
        )
        message = {"text": message}
        for_print.append("Message: %s" % (message))

        if nosend:
            print("nosend set to %s, url: %s" % (nosend, url))
            continue
        else:
            r = requests.post(url, json=message)
            if r.status_code != 200:
                raise Exception("Status %s - content %s" % (r, r.content))
            else:
                if r.text != 'ok':
                    raise Exception(r.text)
                print("Sent to real slack %s: got %s" % (message, r.text[:99]))

    for msg in for_print:
        print(msg)


def download_s3_and_send(filename, topics, filter_, slack_url=None):
    url = os.environ.get("SLACK_HOOK", '')
    datapath = '/tmp/' + filename
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hn.pymi.vn')
    try:
        s3.Object('hn.pymi.vn', filename).load()
    except Exception as e:
        with open(datapath, 'w') as f:
            f.write('')
    else:
        bucket.download_file(filename, datapath)

    slack_send_new_story(url, datapath, topics=topics, filter_=filter_)

    bucket.put_object(ACL='public-read',
                      Bucket='hn.pymi.vn',
                      Key=filename,
                      Body=open(datapath).read().encode(),
                      )


def lambda_handler(event, context):
    filename = 'data.csv'
    download_s3_and_send(filename,
                         topics=hnpy.PYTHON_KEYWORDS,
                         filter_=greater_42)


def send_top_hn(event, context):
    filename = 'top.csv'
    download_s3_and_send(filename,
                         topics=None,
                         filter_=lambda s: s['score'] > 200)


def test():
    import logging
    logging.basicConfig(level=logging.INFO)
    url = ''
    datapath = 'tops.csv'
    slack_send_new_story(url, datapath,
                         topics=None,
                         filter_=lambda s: s['score'] > 200)


if __name__ == "__main__":
    test()
