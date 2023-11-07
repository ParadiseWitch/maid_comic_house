import unittest

from app import app
from spider.spider_factory import SpiderFactory


class TestCopymangaSpider(unittest.TestCase):
    def test_spider_base_comic_info(self):
        with app.app_context():
            copymanga_spider = SpiderFactory().create_spider('copymanga')

            # copymanga_spider.spider_base_comic_info('https://www.copymanga.tv/comic/wojianvyoukebuzhikeaine')
            # chapter_name_and_url_list = copymanga_spider.spider_chapter_list('wojianvyoukebuzhikeaine')
            copymanga_spider.spider_chapter_by_url('https://www.copymanga.tv/comic/wojianvyoukebuzhikeaine/chapter/7006e638-ec89-11e8-b03c-00163e0ca5bd')

unittest.main()
