import os
import sys
from flask import Flask, g
from config.setting import SERVER_PORT
from api.comic import app_comic
from api.index import app_index
from db.db import init_db


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示

app.register_blueprint(app_index, url_prefix="/")
app.register_blueprint(app_comic, url_prefix="/comic")

# 初始化db
init_db(app)


# 应用结束关闭数据库链接
@app.teardown_appcontext
def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# 项目根路径
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_PATH)  # 将项目根路径临时加入环境变量，程序退出后失效

if __name__ == '__main__':
    # host为主机ip地址，port指定访问端口号，debug=True设置调试模式打开
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
