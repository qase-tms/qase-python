import time
import uuid

from typing import Type, Optional, Union, Dict, List
from .basemodel import BaseModel
from .step import Step
from .attachment import Attachment
from .relation import Relation
from .. import QaseUtils


class Field(BaseModel):
    def __init__(self,
                 name: str,
                 value: Union[str, list]):
        self.name = name
        self.value = value


class Execution(BaseModel):
    def __init__(self,
                 status: Optional[str] = None,
                 end_time: int = 0,
                 duration: int = 0,
                 stacktrace: Optional[str] = None,
                 thread: Optional[str] = QaseUtils.get_thread_name()
                 ):
        self.start_time = time.time()
        self.status = status
        self.end_time = end_time
        self.duration = duration
        self.stacktrace = stacktrace
        self.thread = thread

    def set_status(self, status: Optional[str]):
        if status in ['passed', 'failed', 'skipped', 'untested']:
            self.status = status
        else:
            raise ValueError('Step status must be one of: passed, failed, skipped, untested')

    def get_status(self):
        return self.status

    def complete(self):
        self.end_time = time.time()
        self.duration = (int)((self.end_time - self.start_time) * 1000)


class Request(BaseModel):
    def __init__(self,
                 method: str,
                 url: str,
                 status: int,
                 request_headers: Dict[str, str],
                 request_body: str,
                 response_headers: Dict[str, str],
                 response_body: str):
        self.method = method
        self.url = url
        self.status = status
        self.request_headers = request_headers
        self.request_body = request_body
        self.response_headers = response_headers
        self.response_body = response_body


class Result(BaseModel):
    def __init__(self, title: str, signature: str) -> None:
        self.id: str = str(uuid.uuid4())
        self.title: str = title
        self.signature: str = signature
        self.testops_ids: Optional[List[int]] = None
        self.execution: Type[Execution] = Execution()
        self.fields: Dict[Type[Field]] = {}
        self.attachments: List[Attachment] = []
        self.steps: List[Type[Step]] = []
        self.params: Optional[dict] = {}
        self.param_groups: Optional[List[List[str]]] = []
        self.relations: Type[Relation] = None
        self.muted: bool = False
        self.message: Optional[str] = None

    def add_message(self, message: str) -> None:
        self.message = message

    def add_field(self, field: Type[Field]) -> None:
        self.fields[field.name] = field.value

    def add_steps(self, steps: List[Type[Step]]) -> None:
        self.steps = QaseUtils().build_tree(steps)

    def add_attachment(self, attachment: Attachment) -> None:
        self.attachments.append(attachment)

    def add_param(self, key: str, value: str) -> None:
        self.params[key] = value

    def add_param_groups(self, values: List[str]) -> None:
        self.param_groups.append(values)

    def set_relation(self, relation: Relation) -> None:
        self.relations = relation

    def get_status(self) -> Optional[str]:
        return self.execution.status

    def get_id(self) -> str:
        return self.id

    def get_title(self) -> str:
        return self.title

    def get_field(self, name: str) -> Optional[Type[Field]]:
        if name in self.fields:
            return self.fields[name]
        return None

    def get_testops_ids(self) -> Optional[List[int]]:
        return self.testops_ids

    def get_duration(self) -> int:
        return self.execution.duration
