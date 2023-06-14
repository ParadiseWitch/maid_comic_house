from playwright.sync_api import Playwright, sync_playwright, Browser, Page


from comic.comic import Comic
from db.db import query_comic_by_url, update_comic
from index import spider_chapters
from spider.spider import Spider


class CopyComicSpider(Spider):
    host = 'https://www.copymanga.tv/'
    # host = 'https://www.copymanga.site/'
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
        for chapter_item in chapter_list:
            self.spider_chapter_by_url(chapter_item['url'])
        print(chapter_list)
        pass

    def spider_chapter_by_url(self, url: str):
        pass

