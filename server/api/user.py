from flask import Blueprint
from db.db import query_db
import json


app_user = Blueprint("app_user", __name__)


@app_user.route('/<uid>/')
def query_user(uid):
    user = query_db('select * from user where id = ?', args=(uid,), one=True)
    json_str = user['comic']
    json_dict = json.loads(json_str)
    return {
        uid: id,
        json: json_dict
    }


@app_user.route('/add/')
def add_user():
    pass


@app_user.route('/update/<uid>/')
def update_user(uid):
    pass
