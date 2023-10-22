from typing import List
from model.image import Image


class Chapter:
    id: str
    cid: str
    name: str
    url: str
    imgs: List[Image] = []

    def __init__(self, cid: str, url: str, name: str = None):
        self.cid = cid
        self.url = url
        self.name = name
