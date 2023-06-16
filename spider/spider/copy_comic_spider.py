import os
from playwright.sync_api import Playwright, Browser, Page
import requests

from comic.chapter import Chapter
from comic.comic import Comic
from config import DOWNLOAD_PATH
from db.db import query_comic_by_url, update_comic
from spider.spider import Spider


class CopyComicSpider(Spider):
    host = 'https://www.copymanga.tv'
    # host = 'https://www.copymanga.site'
    site = 'copymanga'

    browser: Browser = None
    page: Page = None
    playwright: Playwright

    def __init__(self, browser, page, playwright) -> None:
        self.browser = browser
        self.page = page
        self.playwright = playwright

    def spider_comic_all_chapter(self, url: str):

        self.spider_comic_by_url(url)

    def spider_comic_by_url(self, url: str):
        '''
        爬全部漫画，接着数据库没有的爬
        '''
        # 查数据库
        comic = query_comic_by_url(url)
        if(comic == None):
            comic = Comic()
            comic.url = url
            comic.site = self.site
            comic.id = url.split('/')[-1]

        self.page.goto(url, wait_until='load', timeout=30000)

        comic.name = self.page.eval_on_selector(
            selector='.row > .col-9 > ul > li > h6',
            expression='el => el.textContent || "暂无标题"')

        chapter_list = self.page.eval_on_selector_all(
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

        comic.len = len(chapter_list)
        # 更新comic到数据库
        update_comic(comic)

        print(chapter_list)
        for chapter_item in chapter_list:
            self.spider_chapter_by_url(chapter_item['url'])
        pass

    def spider_chapter_by_url(self, url: str):
        chapter = Chapter()
        chapter.url = url
        # TODO
        chapter.cid = ''
        chapter.name = ''

        chapter_page: Page = self.browser.new_page()
        chapter_page.goto(url)
        chapter_page.set_viewport_size({'width': 1920, 'height': 1080})

        # 获取页数指示器
        chapter_page.wait_for_selector('body > div > .comicCount')
        imgs_len = int(chapter_page.eval_on_selector(
            'body > div > .comicCount', 'el => el.innerText'))

        # 等待漫画内容容器的Dom节点加载
        chapter_page.wait_for_selector(
            '.container-fluid > .container > .comicContent-list')

        # 一直滚动到加载最后一页
        def scroll_to_bottom():
            chapter_page.keyboard.press('PageDown')
            chapter_page.wait_for_timeout(100)
            img_index = int(chapter_page.eval_on_selector(
                'body > div > .comicIndex', 'el => el.innerText'))
            if(img_index >= imgs_len):
                return
            scroll_to_bottom()

        scroll_to_bottom()

        # 获取每页链接
        img_urls: list[str] = chapter_page.eval_on_selector_all(
            '.container-fluid > .container > .comicContent-list > li > img',
            'els => els.map(el => el.getAttribute("data-src"))')

        chapter.images = img_urls

        # TODO保存chapter到数据库

        # TODO下载图片url
        for url in img_urls:
            file_name = url.split('/')[-1]

            down_file_dir = "{}/{}".format(
                DOWNLOAD_PATH, 'output')
            if not os.path.exists(down_file_dir):
                os.makedirs(down_file_dir)

            r = requests.get(url)
            with open(down_file_dir+"/"+file_name, "wb") as f:
                f.write(r.content)

        chapter_page.close()
