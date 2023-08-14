import os
import sys

from flask import Flask, g

from api.index import app_index
from api.comic import app_comic
from api.chapter import app_chapter
from api.user import app_user
from api.image import app_image
from config.setting import SERVER_PORT
from db.db import init_db

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示

app.register_blueprint(app_index, url_prefix="/")
app.register_blueprint(app_comic, url_prefix="/comic")
app.register_blueprint(app_chapter, url_prefix="/chapter")
app.register_blueprint(app_user, url_prefix="/user")
app.register_blueprint(app_image, url_prefix="/image")
# 初始化db
init_db(app)


# 应用结束关闭数据库链接
@app.teardown_appcontext
def close_connection(e):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# 项目根路径
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_PATH)  # 将项目根路径临时加入环境变量，程序退出后失效

if __name__ == '__main__':
    # host为主机ip地址，port指定访问端口号，debug=True设置调试模式打开
    # app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
    
    import json
    text = """
    {"comics": [
        {
             \"id\": 1,
             \"last_read\": 10
        }
    ]}
    """
    j = json.loads(text)
    print(type(j))
    print(j)

    s = json.dumps(j)
    print(type(s))
    print(s)
    




    
