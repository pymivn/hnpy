#!/usr/bin/env python
import json
import logging
import requests
import time
from urllib.parse import urljoin

URL = 'https://hacker-news.firebaseio.com/v0/'
FILE = 'data.json'

logging.basicConfig(filename='getdata.log', level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def _get_json(param):
    url = urljoin(URL, param)
    try:
        res = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        logger.error(url, err)
        return {}
    else:
        return res.json()


def _get_stories_of_topics(topics=None):
    stories = {}
    param_ids = 'topstories.json?print=pretty'
    story_ids = _get_json(param_ids)
    for story_id in story_ids:
        param_id = 'item/{}.json?print=pretty'.format(story_id)
        story = _get_json(param_id)
        if not story:
            continue
        story_title = story.get('title', '')
        story_url = story.get('url', '#')
        logger.debug("Checking story %s: %s", story_title, story_url)
        for kwd in topics:
            if kwd in story_title.lower():
                stories[str(story_id)] = {
                    'title': story_title,
                    'url': story_url
                }
    return stories


def _save_stories(stories):
    with open(FILE, 'w') as outfile:
        json.dump(stories, outfile, indent=4)
    return


def main():
    start_time = time.time()
    topics = ['python', 'django']
    try:
        with open(FILE) as json_data:
            stories = _get_stories_of_topics(topics)
            current_data = json.load(json_data)
    except IOError as err:
        current_data = {}
        logging.error("%s", err)

    current_data.update(stories)
    _save_stories(current_data)
    logging.warning("--Completed in %s seconds.", (time.time() - start_time))


if __name__ == "__main__":
    main()
