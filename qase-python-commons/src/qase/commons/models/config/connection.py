from enum import Enum

from ..basemodel import BaseModel


class Format(Enum):
    json = "json"
    jsonp = "jsonp"


class ConnectionConfig(BaseModel):
    path: str = None
    format: Format = None

    def __init__(self):
        self.format = Format.json
        self.path = "./build/qase-report"

    def set_path(self, path: str):
        self.path = path

    def set_format(self, format: str):
        if any(format == e.value for e in Format.__members__.values()):
            self.format = Format[format]
