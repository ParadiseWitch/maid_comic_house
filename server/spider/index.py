import logging
import os
import time
from playwright.sync_api import Playwright, sync_playwright, Browser, Page

from setting import DOWNLOAD_PATH
from spider.copymanga_spider import CopymangaSpider
from spider.spider import Spider

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
        return CopymangaSpider(playwright)
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
        date_str = time.strftime("%Y-%m-%d", time.localtime())
        logs_dir = '{}/logs/{}'.format(DOWNLOAD_PATH, date_str)

        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        file_info_handler = logging.FileHandler(
            '{}/info.log'.format(logs_dir),
            encoding='utf-8')
        file_info_handler.setLevel(level=logging.INFO)

        file_warn_handler = logging.FileHandler(
            '{}/warn.log'.format(logs_dir),
            encoding='utf-8')
        file_warn_handler.setLevel(level=logging.WARN)

        file_error_handler = logging.FileHandler(
            '{}/error.log'.format(logs_dir),
            encoding='utf-8')
        file_error_handler.setLevel(level=logging.ERROR)

        logging.basicConfig(
            level=logging.INFO,
            encoding='utf-8',
            format='日志生成时间：%(asctime)s  执行文件名：%(filename)s[line:%(lineno)d]  级别：%(levelname)s  输出信息：%(message)s',
            datefmt='%Y-%m-%d %A %H:%M:%S',
            handlers=[file_info_handler, file_warn_handler, file_error_handler])

        site = 'copymanga'
        url = 'https://www.copymanga.tv/comic/haizeiwang'
        # url = 'https://www.copymanga.tv/comic/chubaowangnv'
        spider_comic_all_chapter(url, site, 30)
        # url = 'https://www.copymanga.tv/comic/chaoziranwuzhuangdangdadang'
        # spider_comic_all_chapter(url, site)
        # url = 'https://www.copymanga.tv/comic/jijubukesiyiyanjioubu'
        # spider_comic_all_chapter(url, site)
        # url = 'https://www.copymanga.tv/comic/jiandieguojiajia'
        # spider_comic_all_chapter(url, site)
        # url = 'https://www.copymanga.tv/comic/zgmsbywt'
        # spider_comic_all_chapter(url, site)
        # url = 'https://www.copymanga.tv/comic/nvpengyoujiewoyixia'
        # spider_comic_all_chapter(url, site)
        # url = 'https://www.copymanga.tv/comic/dianjuren'
        # spider_comic_all_chapter(url, site)
        # url = 'https://www.copymanga.tv/comic/xihuanderenwangjidaiyanjle'
        # spider_comic_all_chapter(url, site,site)
        # url = 'https://www.copymanga.tv/comic/wodantuidenvhai/chapter/8148b03c-0699-11ee-a881-d3d228a76de6'
        # spider_chapter_by_url(url, site)
        # url = 'https://www.copymanga.tv/comic/wodantuidenvhai/chapter/ef0a84a8-0b24-11ee-aa3f-d3d228a76de6'
        # spider_chapter_by_url(url, site)

        # spider_chapter_by_url(url, site)
