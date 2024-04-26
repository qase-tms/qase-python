from .basemodel import BaseModel


class RelationSuite(BaseModel):
    def __init__(self, suite_id: int, title: str) -> None:
        self.suite_id = suite_id
        self.title = title


class Relation(BaseModel):
    def __init__(self, type: str, data: RelationSuite):
        self.type = type
        self.data = data
