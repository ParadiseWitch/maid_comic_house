from abc import ABCMeta, abstractmethod
from playwright.sync_api import Playwright, Browser, Page

class Spider(metaclass=ABCMeta):
    browser: Browser
    page: Page
    playwright: Playwright
    host: str
    site: str

    @abstractmethod
    def spider_base_comic_info(self, comic_id: str):
        pass

    def spider_chapter_list(self, comic_id: str):
        pass

    @abstractmethod
    def spider_comic(self, comic_id: str):
        pass

    @abstractmethod
    def spider_chapter_by_url(self, chapter_url: str):
        pass
