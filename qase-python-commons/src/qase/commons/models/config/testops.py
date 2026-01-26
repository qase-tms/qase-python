from .api import ApiConfig
from .batch import BatchConfig
from .plan import PlanConfig
from .run import RunConfig
from ..basemodel import BaseModel
from ... import QaseUtils
from typing import List, Optional


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
    status_filter: List[str] = None
    show_public_report_link: bool = None

    def __init__(self):
        self.api = ApiConfig()
        self.run = RunConfig()
        self.batch = BatchConfig()
        self.plan = PlanConfig()
        self.configurations = ConfigurationsConfig()
        self.defect = False
        self.status_filter = []
        self.show_public_report_link = False

    def set_project(self, project: str):
        self.project = project

    def set_defect(self, defect):
        self.defect = QaseUtils.parse_bool(defect)

    def set_status_filter(self, status_filter: List[str]):
        self.status_filter = status_filter

    def set_show_public_report_link(self, show_public_report_link):
        self.show_public_report_link = QaseUtils.parse_bool(show_public_report_link)


class ProjectConfig(BaseModel):
    code: str = None
    run: RunConfig = None
    plan: PlanConfig = None
    environment: Optional[str] = None

    def __init__(self):
        self.run = RunConfig()
        self.plan = PlanConfig()
        self.environment = None

    def set_code(self, code: str):
        self.code = code

    def set_environment(self, environment: str):
        self.environment = environment

    def set_run(self, run_config: dict):
        """Set run configuration from dictionary"""
        if run_config:
            if 'title' in run_config:
                self.run.set_title(run_config['title'])
            if 'description' in run_config:
                self.run.set_description(run_config['description'])
            if 'complete' in run_config:
                self.run.set_complete(run_config['complete'])
            if 'id' in run_config:
                self.run.set_id(run_config['id'])
            if 'tags' in run_config:
                self.run.set_tags(run_config['tags'])
            if 'externalLink' in run_config:
                self.run.set_external_link(run_config['externalLink'])

    def set_plan(self, plan_config: dict):
        """Set plan configuration from dictionary"""
        if plan_config and 'id' in plan_config:
            self.plan.set_id(plan_config['id'])


class TestopsMultiConfig(BaseModel):
    default_project: Optional[str] = None
    projects: List[ProjectConfig] = None

    def __init__(self):
        self.projects = []
        self.default_project = None

    def set_default_project(self, default_project: str):
        self.default_project = default_project

    def set_projects(self, projects: List[ProjectConfig]):
        self.projects = projects

    def add_project(self, project: ProjectConfig):
        self.projects.append(project)
