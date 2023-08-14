from flask import Blueprint, Response

app_image = Blueprint("app_image", __name__)


@app_image.route('/<id>/')
def query_comic_by_id(id):
    image_stream = ''
    with open('static/logo.jpg', 'rb') as img_f:
        image_stream = img_f.read()
    res = Response(image_stream,mimetype='image/jpeg')
    return res



