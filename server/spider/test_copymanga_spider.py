import unittest

from app import app
from spider.spider_factory import SpiderFactory


class TestCopymangaSpider(unittest.TestCase):
    def test_spider_base_comic_info(self):
        with app.app_context():
            copymanga_spider = SpiderFactory().create_spider('copymanga')
            copymanga_spider.spider_base_comic_info('wojianvyoukebuzhikeaine')


unittest.main()
