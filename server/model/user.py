from model.img import Img


class User:
    id: str
    name: str
    password: str
    avatar: Img
    role: int

    def __init__(self, name, password) -> None:
        self.name = name
        self.password = password
