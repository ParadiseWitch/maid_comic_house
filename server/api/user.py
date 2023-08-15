import logging
from flask import Blueprint, request
from db.db import query_db, update_db
import json


app_user = Blueprint("app_user", __name__)


@app_user.route('/<uid>/')
def query_user(uid):
    user = query_db('select * from user where id = ?', args=(uid,), one=True)
    json_str = user['comics']
    json_dict = json.loads(json_str)
    return {
        "uid": uid,
        "comics": json_dict
    }


@app_user.route('/add/')
def add_user():
    name = request.json['name']
    password = request.json['password']
    comics = request.json['comics'] if request.json['comics'] is None else {}

    # TODO:检查名称是否唯一
    # TODO:加密password
    # TODO:JWT

    update_db('insert into user (name,password,comics) values (?,?,?)',
              args=(name, password, comics))
    return {
        "status": "succ"
    }


@app_user.route('/update_password/<uid>/')
def update_user_psd(uid):
    old_password = request.json['old_password']
    new_password = request.json['new_password']

    # TODO:检查旧密码

    # 更新新密码
    try:
        update_db("""
            update user
            set password = ?
            where id = ?
        """, args=(new_password, id))
    except Exception:
        logging.exception('update user error!')
        return {
            "status": "fail",
            "msg": "insert chapter fail"
        }

    return {
        "status": "succ"
    }
