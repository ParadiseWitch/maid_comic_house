
class Task:
    id: str
    name: str
    status: str  
    info_a: str
    info_b: str
    info_c: str
    info_d: str
    info_e: str
    create_time: str
    start_time: str
    end_time: str

    def __init__(self, name, status) -> None:
        self.name = name
        self.status = status
