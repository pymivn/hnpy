# coding: utf-8
import datetime
from html import escape

import boto3

import util
import template

HTML_NON_BREAKING_SPACE_ENTITY = '&nbsp;'


def render_html(datapath='/tmp/data.csv'):
    current_data = util.get_stories(datapath)
    print("Data loaded from existing db: %s" % current_data)

    with open('/tmp/index.html', 'w') as f:
        f.write(template.HEAD)

        # Newest story first
        for sid, data in sorted(current_data.items(), key=lambda s: s[0], reverse=True):  # NOQA
            data['score'] = data.get('score', 0)
            line = template.LINE.format(
                score='{:4}'.format(data['score']).replace(' ', HTML_NON_BREAKING_SPACE_ENTITY),  # NOQA
                title=escape(data['title']),
                url=escape(data['url']),
                hn_url=escape(util.get_hn_url(sid)),
            )
            f.write(line)

        vn_timezone = datetime.timezone(datetime.timedelta(hours=7))
        render_at = datetime.datetime.now(vn_timezone).strftime(
            "%Y/%m/%d - %H:%M:%S"
        )
        f.write(template.TAIL.format(time=render_at))
    print("Wrote html successfully")


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hn.pymi.vn')
    try:
        s3.Object('hn.pymi.vn', 'data.csv').load()
    except Exception as e:
        print(e)
    else:
        bucket.download_file('data.csv', '/tmp/data.csv')

    render_html()

    bucket.put_object(ACL='public-read',
                      Bucket='hn.pymi.vn',
                      Key='index.html',
                      Body=open('/tmp/index.html').read().encode(),
                      ContentType='text/html; charset=utf-8'
                      )


if __name__ == "__main__":
    render_html('data.csv')
