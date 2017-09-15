'''CSV helper as code will run on AWS Lambda, there is no sqlite3 there.
'''
import csv


def read_csv(csvpath):
    current_data = {}
    try:
        with open(csvpath) as f:
            dr = csv.DictReader(f, ['id', 'url', 'title'])
            for story in dr:
                sid = story.pop('id')
                sid = int(sid)
                current_data[sid] = story
    except IOError as err:
        current_data = {}
    return current_data


def append_csv(csvpath, story):
    with open(csvpath, 'a') as f:
        fields = ['id', 'url', 'title']
        dw = csv.DictWriter(f, fields)
        s = {k: v for k, v in story.items() if k in fields}
        dw.writerow(s)


def pass_through(s):
    return True


def write_new_stories(newstories, oldstory, datapath, condition=None):
    if condition is None:
        condition = pass_through

    for s in newstories:
        if s['id'] not in oldstory:
            if condition(s):
                yield s
                append_csv(datapath, s)


def get_stories(csvpath):
    return read_csv(csvpath)


def get_hn_url(story_id):
    return 'https://news.ycombinator.com/item?id={}'.format(story_id)
