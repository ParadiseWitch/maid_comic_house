import os

import requests
from playwright.sync_api import sync_playwright

from db.db import insert_db, query_db
from logger import mlogger
from model.chapter import Chapter
from model.image import Image
from setting import COMIC_PATH
from spider.spider import Spider
from utils.retry import retry


class CopymangaSpider(Spider):
    host = 'https://www.copymanga.tv'
    # host = 'https://www.copymanga.site'
    site = 'copymanga'
    pw_config = {
        'headless': False,
    }

    def spider_base_comic_info(self, comic_id: str):
        """
        根据url爬取基本漫画信息
        :return:
        """
        # 查询漫画信息是否在数据库中存在
        comic = query_db('select * from comic where id = ?',
                         (comic_id,), one=True)
        if comic is not None:
            mlogger.warning('查询到comic_id={}的漫画已存在，不用再次爬取。'.format(comic_id))
            return
        comic_url = CopymangaSpider.get_url(comic_id)

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.pw_config)
            page = browser.new_page()
            page.set_default_navigation_timeout(30000)
            # page.set_viewport_size({'width': 1920, 'height': 1080})

            mlogger.info('开始爬取漫画信息,id={},site={}'.format(comic_id, self.site))
            page.goto(comic_url, wait_until='load', timeout=30000)
            comic_name = CopymangaSpider.get_comic_name(page)
            comic_desc = CopymangaSpider.get_comic_desc(page)
            authors = CopymangaSpider.get_comic_authors(page)
            tags = CopymangaSpider.get_comic_tags(page)
            last_update_date = CopymangaSpider.get_comic_last_update_date(page)
            comic_status = CopymangaSpider.get_comic_status(page)

            mlogger.info('开始将漫画信息记录到数据库中')
            # 更新作者表
            comic_authors = CopymangaSpider.save_author_db(authors)
            # 更新标签表
            comic_tags = CopymangaSpider.save_tag_db(tags)
            # 插入comic到数据库
            insert_db("""
                insert into comic (id, name,site,desc,url,authors,tags,last_update_date,start_date,status) 
                values (?,?,?,?,?,?,?,?,?,?)
                """, (comic_id, comic_name, self.site,
                      comic_desc, comic_url, comic_authors,
                      comic_tags, last_update_date, None,
                      comic_status), )

            # 关闭页面和浏览器
            page.close()
            browser.close()

    def spider_chapter_list(self, comic_id: str):
        """
        根据漫画id爬取漫画章节url列表
        :param comic_id:
        :return:
        """
        comic_url = self.get_url(comic_id)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_default_navigation_timeout(30000)

            self.page.goto(comic_url, wait_until='load', timeout=30000)
            chapter_name_and_url_list = self.page.eval_on_selector_all(
                selector='#default全部 ul:first-child a',
                expression="""
                    (els, host) =>
                      els.map(el => {
                        return {
                          url: host + el.getAttribute('href'),
                          title: el.textContent || '暂无标题'
                        }
                      })
                    """,
                arg=CopymangaSpider.host)

        mlogger.info('漫画所有章节len={},chapter_list={}'.format(
            len(chapter_name_and_url_list), chapter_name_and_url_list))
        return chapter_name_and_url_list

    def spider_chapter_by_url(self, url: str):
        # 查询
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_default_navigation_timeout(30000)

            comic_id = CopymangaSpider.get_comic_id_by_chapter_url(url)
            # 先爬下有无漫画基本信息
            self.spider_base_comic_info(comic_id)
            mlogger.info('开始下载章节,url={}'.format(url))

            chapter = Chapter(comic_id, url)

            retry(lambda: page.goto(chapter.url))
            page.set_viewport_size({'width': 1920, 'height': 1080})
            mlogger.info('访问章节url成功，url={}'.format(chapter.url))

            # 获取章节名
            titles = page.title().split(' - ')
            comic_name = titles[0]
            chapter.name = titles[1]
            mlogger.info('章节名，name={}'.format(chapter.name))

            # 根据目录按钮链接获取漫画id
            retry(lambda: page.wait_for_selector(
                '.comicContent-prev.list>a'))
            comic_url = page.eval_on_selector(
                '.comicContent-prev.list > a', 'el => el.href')
            chapter.cid = comic_url.split('/')[-1]
            mlogger.info('章节对应漫画id，cid={}'.format(chapter.cid))

            # 获取页数指示器
            retry(lambda: page.wait_for_selector(
                'body > div > .comicCount'))
            imgs_len = int(page.eval_on_selector(
                'body > div > .comicCount', 'el => el.innerText'))
            mlogger.info('本章节页数，len={}'.format(imgs_len))

            # 等待漫画内容容器的Dom节点加载
            retry(lambda: page.wait_for_selector(
                '.container-fluid > .container > .comicContent-list'))
            mlogger.info('漫画内容容器的Dom节点加载成功')

            # 一直滚动到加载最后一页

            CopymangaSpider.scroll_to_bottom(page, imgs_len)
            mlogger.info('滚动结束')

            # 获取每页链接
            retry(lambda: page.wait_for_selector(
                '.container-fluid > .container > .comicContent-list > li > img'))
            img_urls: list[str] = page.eval_on_selector_all(
                '.container-fluid > .container > .comicContent-list > li > img',
                'els => els.map(el => el.getAttribute("data-src"))')
            imgs = []
            for index, item in enumerate(img_urls):
                imgs.append(Image(url=item, name='第{}页'.format(index)))
            imgs = [Image(url=item, name='第{}页'.format(index))
                    for index, item in enumerate(img_urls)]

            chapter.imgs = imgs
            mlogger.info('本章节的所有图片链接，urls={}'.format(img_urls))

            # TODO 保存chapter到数据库

            index = 0
            for url in img_urls:
                index = index + 1
                retry(lambda: CopymangaSpider.down_image(comic_name, chapter.name, url, index,))

            mlogger.info('关闭章节页面成功！章节名，name={}'.format(chapter.name))
            # 关闭网页和浏览器
            page.close()
            browser.close()

    def spider_comic(self, comic_id: str):
        """
        爬全部漫画
        """
        chapter_name_and_url_list = self.spider_chapter_list(comic_id)
        target_chapter_list = []
        for chapter_name_and_url in chapter_name_and_url_list:
            chapter_url = chapter_name_and_url['url']
            chapter_name = chapter_name_and_url['name']
            chapter = Chapter(comic_id, chapter_url, chapter_name)
            chapter.imgs = []
            target_chapter_list.append(chapter)

        mlogger.info('开始爬取章节')
        for chapter_item in target_chapter_list:
            retry(lambda: self.spider_chapter_by_url(chapter_item.url))

    @staticmethod
    def get_url(comic_id: str):
        return '{}/comic/{}'.format(CopymangaSpider.host, comic_id)

    @staticmethod
    def get_comic_id_by_url(url: str):
        if url.endswith('/'):
            url = url[:-1]
        return url.split('/')[-1]

    @staticmethod
    def get_comic_id_by_chapter_url(chapter_url: str):
        if chapter_url.endswith('/'):
            chapter_url = chapter_url[:-1]
        return chapter_url.split('/')[-2]

    @staticmethod
    def get_comic_last_update_date(page):
        last_update_date = page.eval_on_selector(
            selector='ul > li:nth-child(5) > span.comicParticulars-right-txt',
            expression='el => el.textContent')
        return last_update_date

    @staticmethod
    def get_comic_tags(page):
        tags = page.eval_on_selector_all(
            selector='span.comicParticulars-left-theme-all.comicParticulars-tag > a',
            expression="""
                    (els) => els.map(el => el.textContent)
                    """, )
        return tags

    @staticmethod
    def get_comic_authors(page):
        authors = page.eval_on_selector_all(
            selector='ul > li:nth-child(3) > span.comicParticulars-right-txt > a',
            expression="""
                    (els) => els.map(el => el.textContent)
                    """, )
        return authors

    @staticmethod
    def get_comic_desc(page):
        comic_desc = page.eval_on_selector(
            selector='div.container.comicParticulars-synopsis > div:nth-child(2) > p',
            expression='el => el.textContent || "暂无简介"')
        return comic_desc

    @staticmethod
    def get_comic_name(page):
        comic_name = page.eval_on_selector(
            selector='.row > .col-9 > ul > li > h6',
            expression='el => el.textContent || "暂无标题"')
        return comic_name

    @staticmethod
    def save_tag_db(tags):
        comic_tags = []
        for tag_name in tags:
            tag = query_db('select * from tag where name = ?',
                           tag_name, one=True)
            if tag is None:
                insert_db(
                    'insert into tag (name) values (?)', tag_name)
                tag = query_db('select * from tag where name = ?',
                               tag_name, one=True)
            comic_tags.append(tag['id'])
        return comic_tags

    @staticmethod
    def save_author_db(authors):
        comic_authors = []
        for author_name in authors:
            author = query_db('select * from author where name = ?',
                              author_name, one=True)
            if author is None:
                insert_db(
                    'insert into author (name) values (?)', author_name)
                author = query_db('select * from author where name = ?',
                                  author_name, one=True)
            comic_authors.append(author['id'])
        return comic_authors

    @staticmethod
    def get_comic_status(page):
        comic_status = page.eval_on_selector(
            selector='ul > li:nth-child(6) > span.comicParticulars-right-txt',
            expression='el => el.textContent')
        return comic_status

    @staticmethod
    def scroll_to_bottom(page, imgs_len: int):
        page.keyboard.press('PageDown')
        retry(lambda: page.wait_for_timeout(100))
        img_index = int(page.eval_on_selector(
            'body > div > .comicIndex', 'el => el.innerText'))
        mlogger.info('当前页数, img_index={}'.format(img_index))

        if img_index >= imgs_len:
            return
        CopymangaSpider.scroll_to_bottom(page, imgs_len)

    @staticmethod
    def down_image(comic_name, chapter_name, img_url: str, img_index: int):
        """下载文件的方法
        """
        file_name = '第{}页'.format(img_index)
        ext = img_url.split('.')[-1]
        file_name = '{}.{}'.format(file_name, ext)

        down_file_dir = "{}/{}/{}".format(COMIC_PATH,
                                          comic_name, chapter_name)
        if not os.path.exists(down_file_dir):
            os.makedirs(down_file_dir)
            mlogger.info('创建下载文件夹，path={}'.format(down_file_dir))

        target_file_path = down_file_dir + "/" + file_name
        if os.path.exists(target_file_path) and os.path.getsize(target_file_path) > 0:
            mlogger.info(
                '图片已存在, target_file_path={}'.format(target_file_path))
            return
        r = requests.get(img_url, timeout=3 * 60)
        with open(target_file_path, "wb") as f:
            f.write(r.content)
        mlogger.info('下载图片成功！url={}, target_file_path={}'.format(
            img_url, target_file_path))
