import logging
import sqlite3

from flask import Flask, g
from setting import DATABASE


def init_db(app: Flask):
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            try:
                db.cursor().executescript(f.read())
            except Exception as e:
                logging.warning(e)
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def update_db(sql, args=()):
    db = get_db()
    cur = db.execute(sql, args)
    db.commit()
    cur.close()


def insert_db(sql, args=()):
    db = get_db()
    cur = db.execute(sql, args)
    db.commit()
    insert_id = cur.lastrowid
    cur.close()
    return insert_id


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
