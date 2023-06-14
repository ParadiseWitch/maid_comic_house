from playwright.sync_api import Playwright, sync_playwright, Browser, Page

from comic.chapter import Chapter
from spider.copy_comic_spider import CopyComicSpider
from spider.spider import Spider

# host = 'https://www.copymanga.site'
host = 'https://www.copymanga.tv/'
browser: Browser = None
page: Page = None


def initBrowserAndPage():
    global browser, page, playwright
    if (browser and page):
        return
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_default_navigation_timeout(30000)
    page.set_viewport_size({'width': 1920, 'height': 1080})


def get_spider_by_site(site: str) -> Spider:
    if site == 'copymanga':
        return CopyComicSpider(browser, page, playwright)
    raise ValueError('没有找到对应站点的爬虫器！')


def spider_comic_all_chapter(comic_id: str, site: str):
    initBrowserAndPage()
    # 根据site得到spider
    spider = get_spider_by_site(site)
    spider.spider_comic_all_chapter(comic_id)


def spider_chapters(chapter: Chapter):
    '''
    爬哪部漫画哪一个章节
    '''
    comic_url = chapter.comic_url
    chapter_url = chapter.url

    pass


def run(playwright: Playwright) -> None:
    site = 'copymanga'
    url = 'https://www.copymanga.tv/comic/fangxuehoudeouxiangyouyigemimi'
    spider_comic_all_chapter(url, site)


with sync_playwright() as playwright:
    run(playwright)
