from typing import Callable, List

from playwright.sync_api import Playwright, Browser, Page

from model.chapter import Chapter
from model.comic import Comic


class Spider:
    browser: Browser
    page: Page
    playwright: Playwright
    host: str
    site: str

    def init_browser_and_page(self):
        pass

    def close_browser_and_page(self):
        pass

    def spider_base_comic_info_by_url(self):
        pass

    def spider_comic(self, comic: Comic, range_fn: Callable[[List], List]):
        pass

    def spider_chapter_by_url(self, chapter: Chapter):
        pass
