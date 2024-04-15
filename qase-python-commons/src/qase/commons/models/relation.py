class RelationSuite(object):
    def __init__(self, suite_id: int, title: str) -> None:
        self.suite_id = suite_id
        self.title = title

class Relation(object):
    def __init__(self, type: str, data: RelationSuite):
        self.type = type
        self.data = data