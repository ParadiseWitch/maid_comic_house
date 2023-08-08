from flask import Blueprint

app_index = Blueprint("app_index", __name__)


@app_index.route('/')
def home():
    return 'home'
