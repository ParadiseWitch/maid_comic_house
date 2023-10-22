from model.author import Author
from model.chapter import Chapter
from typing import List
from enum import Enum

from model.tag import Tag


class ComicStatus(Enum):
    END = 0
    ING = 1

    @staticmethod
    def get_comic_status(status_str: str):
        """
        获取漫画状态
        :param status_str:
        :return:
        """
        if status_str in ['连载中', '連載中']:
            return ComicStatus.ING
        elif status_str in ['已完结', '已完結']:
            return ComicStatus.END
        else:
            raise Exception('Unknown comic status:{}'.format(status_str))


class Comic:
    id: str
    site: str
    url: str
    name: str
    desc: str
    status: str
    authors: List[Author] = []
    tags: List[Tag] = []
    last_update_date: str
    start_date: str
    chapters: List[Chapter] = []

    def __init__(self, cid, site, url, name, desc) -> None:
        self.id = cid
        self.site = site
        self.url = url
        self.name = name
        self.desc = desc
