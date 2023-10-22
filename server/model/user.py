from model.image import Image


class User:
    id: str
    name: str
    password: str
    avatar: Image
    role: int

    def __init__(self, name, password) -> None:
        self.name = name
        self.password = password
