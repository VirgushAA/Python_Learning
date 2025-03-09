import os as os

os.environ['WIKI_FILE'] = 'wiki.json'


def getenv():
    return os.getenv('WIKI_FILE')
