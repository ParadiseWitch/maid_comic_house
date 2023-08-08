import logging
from flask import Blueprint, request
from db.db import query_db, update_db

app_comic = Blueprint("app_comic", __name__)


@app_comic.route('/<cid>/')
def query_comic_by_id(cid):
    comic = query_db('select * from comic where id = ?', args=(cid), one=True)
    return comic


@app_comic.route('/query/')
def query_comic_by_url():
    url = request.json['url']
    comic = query_db('select * from comic where url = ?', args=(url), one=True)
    return comic


@app_comic.route('/add/', methods=['POST'])
def add_comic():
    site = request.json['site']
    name = request.json['name']
    desc = request.json['desc']
    url = request.json['url']

    try:
        update_db("""
            insert into comic
            (site, name, desc, url)
            values (?, ?, ?, ?)
        """, args=(site, name, desc, url))
    except Exception:
        logging.exception('insert comic error!')
        return {
            "status": "fail",
            "msg": "add comic fail"
        }

    return {
        "status": "succ"
    }


@app_comic.route('/update/<cid>', methods=['POST'])
def update_comic_by_id(cid):
    site = request.json['site']
    name = request.json['name']
    desc = request.json['desc']
    url = request.json['url']

    try:
        update_db("""
            update comic
            set site = ?, name = ?, desc = ?, url = ?
            where id = ?
        """, args=(site, name, desc, url, cid))
    except Exception:
        logging.exception('update comic error!')
        return {
            "status": "fail",
            "msg": "insert comic fail"
        }

    return {
        "status": "succ"
    }
