from ast import List
from comic.chapter import Chapter
from typing import List


class Comic():
    id: str
    site: str = None
    url: str
    name: str = None
    len: int = None
    chapters: List[Chapter] = None
