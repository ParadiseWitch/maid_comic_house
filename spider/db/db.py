
from comic.comic import Comic

import sqlite3


def init():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()

    return


def query_comic_by_url(url: str):
    return None


def update_comic(comic: Comic):
    pass
