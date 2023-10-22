from spider.copymanga_spider import CopymangaSpider
from spider.spider import Spider

spider_map = {
    'copymanga': CopymangaSpider(),
}


class SpiderFactory:
    @staticmethod
    def create_spider(site) -> Spider:
        """
        根据site获取站点
        :param site:
        :return:
        """
        if site in spider_map:
            return spider_map[site]
        raise ValueError('没有找到对应站点的爬虫器！')

    @staticmethod
    def create_spider_by_url(url) -> Spider:
        """
        根据url获取站点
        :param url:
        :return:
        """
        for site in spider_map:
            if site in url:
                return spider_map[site]
        raise ValueError('没有找到对应站点的爬虫器！')
