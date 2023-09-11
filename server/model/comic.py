from model.chapter import Chapter
from typing import List


class Comic():
    id: str
    site: str
    url: str
    name: str
    len: int
    chapters: List[Chapter] = []
