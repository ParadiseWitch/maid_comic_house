import logging
from flask import Blueprint, request
from db.db import query_db, update_db

# TODO: wait for testing


app_chapter = Blueprint("app_chapter", __name__)


@app_chapter.route('/<id>/')
def query_chapter_by_id(id):
    chapter = query_db('select * from chapter where id = ?', args=(id,), one=True)
    return chapter


@app_chapter.route('/query_by_url')
def query_chapter_by_url():
    url = request.args.get('url')
    chapter = query_db('select * from chapter where url = ?', args=(url,), one=True)
    return chapter


@app_chapter.route('/query_by_cid/<cid>/')
def query_chapters_by_cid(cid):
    chapters = query_db('select * from chapter where cid = ?', args=(cid,), one=False)
    return chapters


@app_chapter.route('/add/', methods=['POST'])
def add_chapter():
    cid = request.json['cid']
    name = request.json['name']
    url = request.json['url']

    try:
        update_db("""
            insert into chapter
            (cid, name, url)
            values (?, ?, ?)
        """, args=(cid, name, url))
    except Exception:
        logging.exception('insert chapter error!')
        return {
            "status": "fail",
            "msg": "add chapter fail"
        }

    return {
        "status": "succ"
    }


@app_chapter.route('/update/<id>', methods=['POST'])
def update_chapter_by_id(id):
    cid = request.json['cid']
    name = request.json['name']
    url = request.json['url']

    try:
        update_db("""
            update chapter
            set cid = ?, name = ?, url = ?
            where id = ?
        """, args=(cid, name, url, id))
    except Exception:
        logging.exception('update chapter error!')
        return {
            "status": "fail",
            "msg": "insert chapter fail"
        }

    return {
        "status": "succ"
    }
