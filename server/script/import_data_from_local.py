# 从本地漫画文件导入数据
import logging
import os

from app import app
from db.db import query_db, insert_db
from setting import COMIC_PATH


def loop_comic_path():
    # 获取漫画目录下的所有漫画文件
    for comic_name in os.listdir(COMIC_PATH):
        comic_path = os.path.join(COMIC_PATH, comic_name)
        comic_ctime = os.path.getctime(comic_path)
        comic_mtime = os.path.getmtime(comic_path)
        comic_len = len(os.listdir(comic_path))
        # 更新comic数据库
        comic = query_db('select * from comic where name = ?', args=(comic_name,), one=True)
        if comic is not None:
            logging.warning('comic {} already exists in db', comic_name)
            continue
        comic_id = insert_db('insert into comic (name,start_date,last_update_date,len,site) values (?,?,?,?,?)',
                             args=(comic_name, comic_ctime, comic_mtime, comic_len, 'copymanga'))
        for chapter_name in os.listdir(comic_path):
            chapter_path = os.path.join(comic_path, chapter_name)
            # 更新chapter数据库
            chapter = query_db('select * from chapter where name = ? and cid = ?', args=(comic_name, comic_id), one=True)
            if chapter is not None:
                logging.warning('chapter {} already exists in db', chapter_path)
                continue
            chapter_id = insert_db('insert into chapter (cid,name) values (?,?)', args=(comic_id, chapter_name))
            for img_name in os.listdir(chapter_path):
                img_path = '{}/{}/{}'.format(comic_name, chapter_name, img_name)
                # 更新image数据库
                insert_db('insert into image (cid,name) values (?,?)', args=(chapter_id, img_name))


if __name__ == '__main__':
    with app.app_context():
        loop_comic_path()
