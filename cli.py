import argparse
import logging
import time

import hnpy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def main():

    argp = argparse.ArgumentParser()
    argp.add_argument('keyword',
                      help='list of keywords to search for on titles',
                      type=str,
                      nargs='*',
                      default=[])
    args = argp.parse_args()

    keywords = args.keyword or hnpy.PYTHON_KEYWORDS
    logger.info("Getting keywords %s", keywords)
    start_time = time.time()
    for story in hnpy.get_stories_on_topic(keywords):
        print('{0}. {1:4>} score - {2} {3}'.format(
              hnpy.get_hn_url(story['id']),
              story['score'], story['title'], story['url']
              ))

    logger.info("--Completed in %s seconds.", (time.time() - start_time))


if __name__ == "__main__":
    main()
