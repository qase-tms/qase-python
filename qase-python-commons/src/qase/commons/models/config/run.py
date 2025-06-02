from typing import List
from ..basemodel import BaseModel
from ... import QaseUtils


class RunConfig(BaseModel):
    title: str = None
    description: str = None
    complete: bool = None
    id: int = None
    tags: List[str] = None


    def __init__(self):
        self.complete = True
        self.tags = []

    def set_title(self, title: str):
        self.title = title

    def set_description(self, description: str):
        self.description = description

    def set_complete(self, complete):
        self.complete = QaseUtils.parse_bool(complete)

    def set_id(self, id: int):
        self.id = id

    def set_tags(self, tags: List[str]):
        self.tags = tags
