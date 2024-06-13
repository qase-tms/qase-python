from ..basemodel import BaseModel


class RunConfig(BaseModel):
    title: str = None
    description: str = None
    complete: bool = None
    id: int = None

    def __init__(self):
        self.complete = True

    def set_title(self, title: str):
        self.title = title

    def set_description(self, description: str):
        self.description = description

    def set_complete(self, complete: bool):
        self.complete = complete

    def set_id(self, id: int):
        self.id = id
