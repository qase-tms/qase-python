from enum import Enum

from .connection import ConnectionConfig
from ..basemodel import BaseModel


class Driver(Enum):
    local = "local"


class ReportConfig(BaseModel):
    driver: Driver = None
    connection: ConnectionConfig = None

    def __init__(self):
        self.driver = Driver.local
        self.connection = ConnectionConfig()

    def set_driver(self, driver: str):
        if any(driver == e.value for e in Driver.__members__.values()):
            self.driver = Driver[driver]
