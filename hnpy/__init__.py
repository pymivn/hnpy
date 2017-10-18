#!/usr/bin/env python
import concurrent.futures
import logging

from urllib.parse import urljoin

import requests


URL = 'https://hacker-news.firebaseio.com/v0/'

logger = logging.getLogger(__name__)
# ython will match python, jython ...
PYTHON_KEYWORDS = [
    'ython', 'pypy', 'scipy', 'numpy', 'pandas',
    'flask', 'django', 'pypi',
]


def get_hn_url(story_id):
    return 'https://news.ycombinator.com/item?id={}'.format(story_id)


def get_story(story_id):
    # E.g https://hacker-news.firebaseio.com/v0/item/15164948.json?print=pretty
    param = 'item/{}.json?print=pretty'.format(story_id)
    url = urljoin(URL, param)
    try:
        logger.debug("Getting URL %s", url)
        res = requests.get(url)
    except Exception as err:
        logger.error("Error: %s %s", url, err)
        return {}
    else:
        story = res.json()
        if story:
            return story
        else:
            return {}


def hn_top_stories_ids():
    url = urljoin(URL, 'topstories.json?print=pretty')
    try:
        logger.debug("Getting %s", url)
        story_ids = requests.get(url).json()
        logger.info("Got total %d top stories", len(story_ids))
    except Exception as err:
        logger.critical("Cannot get list of top stories from HN: %r", err)
        raise

    for story_id in story_ids:
        yield story_id


def top_stories():
    '''Get top stories from HN'''
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for res in executor.map(get_story, hn_top_stories_ids()):
            if res:
                res['url'] = res.get('url', get_hn_url(res['id']))
                yield res


def get_stories_on_topic(keywords=None):
    for story in top_stories():
        logger.debug("Checking story %d %s: %s",
                     story['score'], story['title'], story['url'])
        if keywords:
            keywords = [k.lower() for k in keywords]
            story_title = story['title']
            for kwd in keywords:
                if kwd in story_title.lower():
                    yield story
        else:
            yield story
