import os
import sys
from typing import List, Callable

import requests
from playwright.sync_api import Playwright, Browser, Page, sync_playwright

from logger import mlogger
from db.comic_db import update_comic
from db.db import query_db
from model.chapter import Chapter
from model.comic import Comic, ComicStatus
from model.image import Image
from setting import COMIC_PATH
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

    def get_url(self, comic_id: str):
        return '{}/comic/{}'.format(self.host, comic_id)

    def init_browser_and_page(self):
        if (self.playwright is not None
                and self.browser is not None
                and self.page is not None):
            return
        with sync_playwright() as p:
            self.playwright = p
            self.browser = self.playwright.chromium.launch(headless=True)
            self.page = self.browser.new_page()
            self.page.set_default_navigation_timeout(30000)
            self.page.set_viewport_size({'width': 1920, 'height': 1080})

    def close_browser_and_page(self):
        self.browser.close()
        self.page.close()

    def spider_base_comic_info(self, comic_id: str):
        """
        根据url爬取基本漫画信息
        :return:
        """
        comic = query_db('select * from comic where id = ?', comic_id, one=True)
        if comic is not None:
            mlogger.warning('查询到comic_id={}的漫画已存在。不用再次爬取'.format(comic_id))
            return
        comic_url = self.get_url(comic_id)
        mlogger.info('开始爬取漫画信息,id={},site={}'.format(comic_id, self.site))
        self.page.goto(comic_url, wait_until='load', timeout=30000)
        comic_name = self.page.eval_on_selector(
            selector='.row > .col-9 > ul > li > h6',
            expression='el => el.textContent || "暂无标题"')
        mlogger.info('漫画名:{}'.format(comic_name))

        comic_desc = self.page.eval_on_selector(
            selector='div.container.comicParticulars-synopsis > div:nth-child(2) > p',
            expression='el => el.textContent || "暂无简介"'
        )
        authors = self.page.eval_on_selector_all(
            selector='ul > li:nth-child(3) > span.comicParticulars-right-txt > a',
            expression="""
                (els) => els.map(el => el.textContent)
                """, )
        tags = self.page.eval_on_selector_all(
            selector='span.comicParticulars-left-theme-all.comicParticulars-tag > a',
            expression="""
                (els) => els.map(el => el.textContent)
                """, )
        last_update_date = self.page.eval_on_selector(
            selector='ul > li:nth-child(5) > span.comicParticulars-right-txt',
            expression='el => el.textContent'
        )
        comic_status = self.page.eval_on_selector(
            selector='ul > li:nth-child(6) > span.comicParticulars-right-txt',
            expression='el => el.textContent'
        )
        mlogger.info('开始将漫画信息记录到数据库中')

        # 更新comic到数据库
        comic = Comic(comic_id, self.site, comic_url, comic_name, comic_desc)
        comic.last_update_date = last_update_date
        comic.start_date = None
        comic.status = ComicStatus.get_comic_status(comic_status)
        # TODO 先查后插入
        query_db('select * from comic where id = ?', comic_id, one=True)
        comic.authors = authors
        comic.authors = tags
        update_comic(comic)

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

        mlogger.info('漫画所有章节len={},chapter_list={}'.format(
            len(chapter_name_and_url_list), chapter_name_and_url_list))
        return chapter_name_and_url_list


def spider_comic(self, comic_id: str):
    """
    爬全部漫画
    """
    chapter_name_and_url_list = self.spider_base_comic_info(comic_id)
    target_chapter_list = []
    for chapter_name_and_url in chapter_name_and_url_list:
        chapter_url = chapter_name_and_url['url']
        chapter_name = chapter_name_and_url['name']
        chapter = Chapter(comic_id, chapter_url, chapter_name)
        chapter.imgs = []
        target_chapter_list.append(chapter)

    mlogger.info('开始爬取章节')
    for chapter_item in target_chapter_list:
        retry(lambda: self.spider_chapter_by_url(chapter_item))


def spider_chapter_by_url(self, url: str):
    # 查询
    comic_id = url.split('/')[-1]
    self.spider_base_comic_info(comic_id)
    mlogger.info('开始下载章节,url={}'.format(url))

    chapter = Chapter(comic_id, url)

    if self.chapter_page is not None:
        self.chapter_page.close()
    self.chapter_page = self.browser.new_page()

    retry(lambda: self.chapter_page.goto(chapter.url))
    self.chapter_page.set_viewport_size({'width': 1920, 'height': 1080})
    mlogger.info('访问章节url成功，url={}'.format(chapter.url))

    # 获取章节名
    titles = self.chapter_page.title().split(' - ')
    comic_name = titles[0]
    chapter.name = titles[1]
    mlogger.info('章节名，name={}'.format(chapter.name))

    # 根据目录按钮链接获取漫画id
    retry(lambda: self.chapter_page.wait_for_selector(
        '.comicContent-prev.list>a'))
    comic_url = self.chapter_page.eval_on_selector(
        '.comicContent-prev.list > a', 'el => el.href')
    chapter.cid = comic_url.split('/')[-1]
    mlogger.info('章节对应漫画id，cid={}'.format(chapter.cid))

    # 获取页数指示器
    retry(lambda: self.chapter_page.wait_for_selector(
        'body > div > .comicCount'))
    imgs_len = int(self.chapter_page.eval_on_selector(
        'body > div > .comicCount', 'el => el.innerText'))
    mlogger.info('本章节页数，len={}'.format(imgs_len))

    # 等待漫画内容容器的Dom节点加载
    retry(lambda: self.chapter_page.wait_for_selector(
        '.container-fluid > .container > .comicContent-list'))
    mlogger.info('漫画内容容器的Dom节点加载成功')

    # 一直滚动到加载最后一页
    def scroll_to_bottom():
        self.chapter_page.keyboard.press('PageDown')
        retry(lambda: self.chapter_page.wait_for_timeout(100))
        img_index = int(self.chapter_page.eval_on_selector(
            'body > div > .comicIndex', 'el => el.innerText'))
        mlogger.info('当前页数, img_index={}'.format(img_index))

        if img_index >= imgs_len:
            return
        scroll_to_bottom()

    scroll_to_bottom()
    mlogger.info('滚动结束')

    # 获取每页链接
    retry(lambda: self.chapter_page.wait_for_selector(
        '.container-fluid > .container > .comicContent-list > li > img'))
    img_urls: list[str] = self.chapter_page.eval_on_selector_all(
        '.container-fluid > .container > .comicContent-list > li > img',
        'els => els.map(el => el.getAttribute("data-src"))')
    imgs = []
    for index, item in enumerate(img_urls):
        imgs.append(Image(url=item, name='第{}页'.format(index)))
    imgs = [Image(url=item, name='第{}页'.format(index)) for index, item in enumerate(img_urls)]

    chapter.imgs = imgs
    mlogger.info('本章节的所有图片链接，urls={}'.format(img_urls))

    # TODO 保存chapter到数据库
    def down_image(img_url: str, index: int):
        """下载文件的方法
        """
        file_name = '第{}页'.format(index)
        ext = img_url.split('.')[-1]
        file_name = '{}.{}'.format(file_name, ext)

        down_file_dir = "{}/{}/{}".format(COMIC_PATH,
                                          comic_name, chapter.name)
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
            url, target_file_path))

    index = 0
    for url in img_urls:
        index = index + 1
        retry(lambda: down_image(url, index))

    mlogger.info('关闭章节页面成功！章节名，name={}'.format(chapter.name))
    self.chapter_page.close()
