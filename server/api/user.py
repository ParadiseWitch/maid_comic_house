from flask import Blueprint


app_user = Blueprint("app_user", __name__)


@app_user.route('/<uid>/')
def query_user(uid):
    pass


@app_user.route('/add/')
def add_user():
    pass


@app_user.route('/update/<uid>/')
def update_user(uid):
    pass
