from abc import ABCMeta, abstractmethod
from typing import Callable, List

from playwright.sync_api import Playwright, Browser, Page

from model.chapter import Chapter
from model.comic import Comic


class Spider(metaclass=ABCMeta):
    browser: Browser
    page: Page
    playwright: Playwright
    host: str
    site: str

    @abstractmethod
    def init_browser_and_page(self):
        pass

    @abstractmethod
    def close_browser_and_page(self):
        pass

    @abstractmethod
    def get_url(self, comic_id:str):
        pass

    @abstractmethod
    def spider_base_comic_info(self, comic_id: str):
        pass

    @abstractmethod
    def spider_comic(self, comic: Comic, range_fn: Callable[[List], List]):
        pass

    @abstractmethod
    def spider_chapter_by_url(self, url: str):
        pass
