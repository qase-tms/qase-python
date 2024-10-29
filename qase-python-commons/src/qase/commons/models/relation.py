from .basemodel import BaseModel


class SuiteData(BaseModel):
    def __init__(self, title: str) -> None:
        self.public_id = None
        self.title = title


class RelationSuite(BaseModel):
    def __init__(self) -> None:
        self.data = []

    def add_data(self, data: SuiteData) -> None:
        self.data.append(data)


class Relation(BaseModel):
    def __init__(self):
        self.suite = RelationSuite()

    def add_suite(self, suite: SuiteData) -> None:
        self.suite.add_data(suite)
