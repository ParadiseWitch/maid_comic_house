from re import A


class Image:
    id: str
    cid: str
    name: str
    url: str

    def __init__(self, url, name):
        self.url = url
        self.name = name
