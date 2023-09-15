import logging
import os
import sys
from typing import List, Callable

import requests
from playwright.sync_api import Playwright, Browser, Page

from db.comic_db import update_comic
from model.chapter import Chapter
from model.comic import Comic
from setting import DOWNLOAD_PATH
from spider.spider import Spider
from utils.retry import retry


class CopymangaSpider(Spider):
    browser: Browser
    page: Page
    playwright: Playwright
    host = 'https://www.copymanga.tv'
    # host = 'https://www.copymanga.site'
    site = 'copymanga'
    browser: Browser = None
    page: Page = None
    chapter_page: Page = None
    playwright: Playwright

    def __init__(self, playwright: Playwright) -> None:
        self.playwright = playwright

    def init_browser_and_page(self):
        if self.browser is not None and self.page is not None:
            return
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        self.page.set_default_navigation_timeout(30000)
        self.page.set_viewport_size({'width': 1920, 'height': 1080})

    def close_browser_and_page(self):
        self.browser.close()
        self.page.close()

    def spider_base_comic_info_by_url(self):
        """
        根据url爬取基本漫画信息
        :return:
        """
        pass

    def spider_comic(self, comic: Comic, range_fn: Callable[[List], List] = lambda arr: arr[0:sys.maxsize]):
        """
        爬全部漫画
        """
        logging.info('开始下载漫画,url={}'.format(comic.url))
        self.page.goto(comic.url, wait_until='load', timeout=30000)
        comic.name = self.page.eval_on_selector(
            selector='.row > .col-9 > ul > li > h6',
            expression='el => el.textContent || "暂无标题"')
        logging.info('漫画名:{}'.format(comic.name))
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
            arg=self.host)

        comic.len = len(chapter_name_and_url_list)
        logging.info('漫画所有章节len={},chapter_list={}'.format(comic.len, chapter_name_and_url_list))
        # 更新comic到数据库 # TODO 耦合
        update_comic(comic)
        target_chapter_name_and_url_list = range_fn(chapter_name_and_url_list)

        def map_chapter_list(chapter_name_and_url):
            chapter_url = chapter_name_and_url['url']
            chapter_name = chapter_name_and_url['name']
            chapter = Chapter()
            chapter.cid = comic.id
            chapter.url = chapter_url
            chapter.name = chapter_name
            chapter.images = []
            return chapter

        target_chapter_list = list(map(map_chapter_list, target_chapter_name_and_url_list))
        logging.info('开始爬取章节')
        for chapter_item in target_chapter_list:
            retry(lambda: self.spider_chapter_by_url(chapter_item))

    def spider_chapter_by_url(self, chapter: Chapter):
        logging.info('开始下载章节,name={},url={}'.format(chapter.name, chapter.url))

        if self.chapter_page is not None:
            self.chapter_page.close()
        self.chapter_page: Page = self.browser.new_page()

        retry(lambda: self.chapter_page.goto(chapter.url))
        self.chapter_page.set_viewport_size({'width': 1920, 'height': 1080})
        logging.info('访问章节url成功，url={}'.format(chapter.url))

        # 获取章节名
        titles = self.chapter_page.title().split(' - ')
        comic_name = titles[0]
        chapter.name = titles[1]
        logging.info('章节名，name={}'.format(chapter.name))

        # 根据目录按钮链接获取漫画id
        retry(lambda: self.chapter_page.wait_for_selector(
            '.comicContent-prev.list>a'))
        comic_url = self.chapter_page.eval_on_selector(
            '.comicContent-prev.list > a', 'el => el.href')
        chapter.cid = comic_url.split('/')[-1]
        logging.info('章节对应漫画id，cid={}'.format(chapter.cid))

        # 获取页数指示器
        retry(lambda: self.chapter_page.wait_for_selector(
            'body > div > .comicCount'))
        imgs_len = int(self.chapter_page.eval_on_selector(
            'body > div > .comicCount', 'el => el.innerText'))
        logging.info('本章节页数，len={}'.format(imgs_len))

        # 等待漫画内容容器的Dom节点加载
        retry(lambda: self.chapter_page.wait_for_selector(
            '.container-fluid > .container > .comicContent-list'))
        logging.info('漫画内容容器的Dom节点加载成功')

        # 一直滚动到加载最后一页
        def scroll_to_bottom():
            self.chapter_page.keyboard.press('PageDown')
            retry(lambda: self.chapter_page.wait_for_timeout(100))
            img_index = int(self.chapter_page.eval_on_selector(
                'body > div > .comicIndex', 'el => el.innerText'))
            logging.info('当前页数, img_index={}'.format(img_index))

            if img_index >= imgs_len:
                return
            scroll_to_bottom()

        scroll_to_bottom()
        logging.info('滚动结束')

        # 获取每页链接
        retry(lambda: self.chapter_page.wait_for_selector(
            '.container-fluid > .container > .comicContent-list > li > img'))
        img_urls: list[str] = self.chapter_page.eval_on_selector_all(
            '.container-fluid > .container > .comicContent-list > li > img',
            'els => els.map(el => el.getAttribute("data-src"))')

        chapter.images = img_urls
        logging.info('本章节的所有图片链接，urls={}'.format(chapter.images))

        # TODO 保存chapter到数据库
        def down_image(img_url: str, index: int):
            """下载文件的方法
            """
            file_name = '第{}页'.format(index)
            ext = img_url.split('.')[-1]
            file_name = '{}.{}'.format(file_name, ext)

            down_file_dir = "{}/comic/{}/{}".format(DOWNLOAD_PATH,
                                                    comic_name, chapter.name)
            if not os.path.exists(down_file_dir):
                os.makedirs(down_file_dir)
                logging.info('创建下载文件夹，path={}'.format(down_file_dir))

            target_file_path = down_file_dir + "/" + file_name
            if os.path.exists(target_file_path) and os.path.getsize(target_file_path) > 0:
                logging.info(
                    '图片已存在, target_file_path={}'.format(target_file_path))
                return

            r = requests.get(img_url, timeout=3 * 60)
            with open(target_file_path, "wb") as f:
                f.write(r.content)
            logging.info('下载图片成功！url={}, target_file_path={}'.format(
                url, target_file_path))

        index = 0
        for url in img_urls:
            index = index + 1
            retry(lambda: down_image(url, index))

        logging.info('关闭章节页面成功！章节名，name={}'.format(chapter.name))
        self.chapter_page.close()