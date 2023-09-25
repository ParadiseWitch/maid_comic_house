from typing import List
from model.img import Img


class Chapter:
    id: str
    cid: str
    name: str
    url: str
    imgs: List[Img] = []

    def __init__(self, cid, name, url) -> None:
        self.cid = cid
        self.name = name
        self.url = url