import logging
import os
import time
from playwright.sync_api import Playwright, sync_playwright, Browser, Page

from setting import LOGGER_PATH
from spider.copymanga_spider import CopymangaSpider
from spider.spider import Spider
from spider.spider_factory import SpiderFactory

# host = 'https://www.copymanga.site'
# host = 'https://www.copymanga.tv'
browser: Browser
page: Page
playwright: Playwright


def init_browser_and_page():
    global browser, page
    # if (browser != None and page != None):
    #     return
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_default_navigation_timeout(30000)
    page.set_viewport_size({'width': 1920, 'height': 1080})


def get_spider_by_site(site: str) -> Spider:
    if site == 'copymanga':
        return CopymangaSpider()
    raise ValueError('没有找到对应站点的爬虫器！')


def spider_comic_all_chapter(comic_id: str, site: str, range_fn):
    spider = get_spider_by_site(site)
    # 初始化
    spider.init_browser_and_page()
    # TODO 根据site得到spider
    spider.spider_comic(comic_id, range_fn)


def spider_chapter_by_url(url: str, site: str):
    """
    爬哪部漫画哪一个章节
    """
    init_browser_and_page()
    # 根据site得到spider
    spider = get_spider_by_site(site)
    spider.spider_chapter_by_url(url)

    pass


def run() -> None:
    global playwright
    with sync_playwright() as p:
        playwright = p

        url = 'https://www.copymanga.tv/comic/haizeiwang'
        # url = 'https://www.copymanga.tv/comic/chubaowangnv'

        spider = SpiderFactory.create_spider(url)
        spider.spider_chapter_by_url(url)
