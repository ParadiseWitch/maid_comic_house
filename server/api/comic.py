import logging
from flask import Blueprint, request
from db.db import query_db, update_db

app_comic = Blueprint("app_comic", __name__)


@app_comic.route('/<id>/')
def query_comic_by_id(id):
    comic = query_db('select * from comic where id = ?', args=(id,), one=True)
    return comic


@app_comic.route('/query/')
def query_comic_by_url():
    url = request.json['url']
    comic = query_db('select * from comic where url = ?', args=(url,), one=True)
    return comic


@app_comic.route('/add/', methods=['POST'])
def add_comic():
    id = request.json['id']
    site = request.json['site']
    name = request.json['name']
    desc = request.json['desc']
    url = request.json['url']

    try:
        update_db("""
            insert into comic
            (id, site, name, desc, url)
            values (?, ?, ?, ?, ?)
        """, args=(id, site, name, desc, url,))
    except Exception:
        logging.exception('insert comic error!')
        return {
            "status": "fail",
            "msg": "add comic fail"
        }

    return {
        "status": "succ"
    }


@app_comic.route('/update/<id>', methods=['POST'])
def update_comic_by_id(id):
    site = request.json['site']
    name = request.json['name']
    desc = request.json['desc']
    url = request.json['url']

    try:
        update_db("""
            update comic
            set site = ?, name = ?, desc = ?, url = ?
            where id = ?
        """, args=(site, name, desc, url, id,))
    except Exception:
        logging.exception('update comic error!')
        return {
            "status": "fail",
            "msg": "insert comic fail"
        }

    return {
        "status": "succ"
    }
