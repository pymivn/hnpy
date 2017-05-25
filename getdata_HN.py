#!/usr/bin/env python
import json
import logging
import requests
import time
from urllib.parse import urljoin

URL = 'https://hacker-news.firebaseio.com/v0/'
FILE = 'data.json'


def _get_json(param):
    url = urljoin(URL, param)
    try:
        res = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        logging.error(err)
    return res.json()


def _get_stories_of_topics(topics=None):
    stories = {}
    param_ids = 'topstories.json?print=pretty'
    story_ids = _get_json(param_ids)
    for story_id in story_ids:
        param_id = 'item/{}.json?print=pretty'.format(story_id)
        story = _get_json(param_id)
        story_title = story.get('title', '')
        for kwd in topics:
            if kwd in story_title.lower():
                story_url = story.get('url', '#')
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
    logging.basicConfig(filename='getdata.log', level=logging.WARNING)
    topics = ['python', 'django']
    with open(FILE) as json_data:
        stories = _get_stories_of_topics(topics)
        try:
            current_data = json.load(json_data)
        except IOError as err:
            current_data = {}
            logging.error(err)
        current_data.update(stories)
    _save_stories(stories)
    logging.warning("--Completed in %s seconds." % (time.time() - start_time))


if __name__ == "__main__":
    main()
