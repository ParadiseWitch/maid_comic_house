from model.author import Author
from model.chapter import Chapter
from typing import List

from model.tag import Tag


class Comic:
    id: str
    site: str
    url: str
    name: str
    desc: str
    author: Author
    tags: List[Tag] = []
    chapters: List[Chapter] = []

    def __init__(self, site, url, name, desc) -> None:
        self.site = site
        self.url = url
        self.name = name
        self.desc = desc
