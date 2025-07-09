from .api import ApiConfig
from .batch import BatchConfig
from .plan import PlanConfig
from .run import RunConfig
from ..basemodel import BaseModel
from ... import QaseUtils
from typing import List


class ConfigurationValue(BaseModel):
    name: str = None
    value: str = None

    def __init__(self, name: str = None, value: str = None):
        self.name = name
        self.value = value

    def set_name(self, name: str):
        self.name = name

    def set_value(self, value: str):
        self.value = value


class ConfigurationsConfig(BaseModel):
    values: List[ConfigurationValue] = None
    create_if_not_exists: bool = None

    def __init__(self):
        self.values = []
        self.create_if_not_exists = False

    def set_values(self, values: List[ConfigurationValue]):
        self.values = values

    def set_create_if_not_exists(self, create_if_not_exists):
        self.create_if_not_exists = QaseUtils.parse_bool(create_if_not_exists)

    def add_value(self, name: str, value: str):
        self.values.append(ConfigurationValue(name=name, value=value))


class TestopsConfig(BaseModel):
    project: str = None
    defect: bool = None
    api: ApiConfig = None
    run: RunConfig = None
    plan: PlanConfig = None
    batch: BatchConfig = None
    configurations: ConfigurationsConfig = None

    def __init__(self):
        self.api = ApiConfig()
        self.run = RunConfig()
        self.batch = BatchConfig()
        self.plan = PlanConfig()
        self.configurations = ConfigurationsConfig()
        self.defect = False

    def set_project(self, project: str):
        self.project = project

    def set_defect(self, defect):
        self.defect = QaseUtils.parse_bool(defect)
