from spider.spider import Spider


class CopyComicSpider(Spider):
    site = 'copycomic'
    host = 'https://www.copycomic.site/'

    def spider_comic_all_chapter(comic_id: str):
        # comic = query_comic_by_site_and_id();
        # old_len = comic.len
        # new_len = spdier_comic_len(comid_id, site)
        # 判断oldlen和newlen
        pass

