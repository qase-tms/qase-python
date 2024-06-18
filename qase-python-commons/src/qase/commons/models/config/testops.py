from .api import ApiConfig
from .batch import BatchConfig
from .plan import PlanConfig
from .run import RunConfig
from ..basemodel import BaseModel
from ... import QaseUtils


class TestopsConfig(BaseModel):
    project: str = None
    defect: bool = None
    api: ApiConfig = None
    run: RunConfig = None
    plan: PlanConfig = None
    batch: BatchConfig = None

    def __init__(self):
        self.api = ApiConfig()
        self.run = RunConfig()
        self.batch = BatchConfig()
        self.plan = PlanConfig()
        self.defect = False
        self.use_v2 = False

    def set_project(self, project: str):
        self.project = project

    def set_defect(self, defect):
        self.defect = QaseUtils.parse_bool(defect)

    def set_use_v2(self, use_v2):
        self.use_v2 = QaseUtils.parse_bool(use_v2)
