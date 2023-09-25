from re import A


class Img():
    id: str
    cid: str
    path: str
    url: str

    def __init__(self, url, path):
        self.url = url
        self.path = path
