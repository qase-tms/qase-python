import time
import uuid

from enum import Enum
from typing import Optional, Union, Dict, List, Type
from .attachment import Attachment
from .basemodel import BaseModel


class StepType(Enum):
    TEXT = 'text'
    ASSERT = 'assert'
    GHERKIN = 'gherkin'
    REQUEST = 'request'
    DB_QUERY = 'db_query'
    SLEEP = 'sleep'


class StepTextData(BaseModel):
    def __init__(self, action: str, expected_result: Optional[str] = None):
        self.action = action
        self.expected_result = expected_result


class StepAssertData(BaseModel):
    def __init__(self, expected: str, actual: str, message: str):
        self.expected = expected
        self.actual = actual
        self.message = message


class StepGherkinData(BaseModel):
    def __init__(self, keyword: str, name: str, line: int):
        self.keyword = keyword
        self.name = name
        self.line = line


class StepRequestData(BaseModel):
    def __init__(self, request_body: str, request_headers: Dict[str, str], request_method: str, request_url: str):
        self.response_headers = None
        self.response_body = None
        self.status_code = None
        if isinstance(request_body, bytes):
            request_body = request_body.decode('utf-8')
        self.request_body = request_body
        if isinstance(request_headers, bytes):
            request_headers = request_headers.decode('utf-8')
        self.request_headers = request_headers
        self.request_method = request_method
        self.request_url = request_url

    def add_response(self, status_code: int, response_body: Optional[str] = None,
                     response_headers: Optional[Dict[str, str]] = None):
        self.status_code = status_code

        if isinstance(response_body, bytes):
            response_body = response_body.decode('utf-8')
        self.response_body = response_body
        if isinstance(response_headers, bytes):
            response_headers = response_headers.decode('utf-8')
        self.response_headers = response_headers


class StepDbQueryData(BaseModel):
    def __init__(self, query: str, expected_result: str):
        self.query = query


class StepSleepData(BaseModel):
    def __init__(self, duration: int):
        self.duration = duration


class StepExecution(BaseModel):
    def __init__(self, status: Optional[str] = 'untested', end_time: int = 0, duration: int = 0):
        self.start_time = time.time()
        self.status = status
        self.end_time = end_time
        self.duration = duration

    def set_status(self, status: Optional[str]):
        if status in ['passed', 'failed', 'skipped', 'blocked', 'untested']:
            self.status = status
        else:
            raise ValueError('Step status must be one of: passed, failed, skipped, blocked, untested')

    def complete(self):
        self.end_time = time.time()
        self.duration = int((self.end_time - self.start_time) * 1000)


class Step(BaseModel):
    def __init__(self,
                 step_type: StepType,
                 id: Optional[str],
                 data: Optional[
                     Union[StepTextData, StepAssertData, StepGherkinData, StepRequestData, StepSleepData]] = None,
                 parent_id: Optional[str] = None
                 ):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())

        self.step_type = step_type
        self.data = data
        self.parent_id = parent_id
        self.execution = StepExecution()
        self.attachments = []
        self.steps = []

    def set_parent_id(self, parent_id: Optional[str]):
        self.parent_id = parent_id

    def get_parent_id(self) -> Optional[str]:
        return self.parent_id

    def get_steps(self, as_dict: bool = False):
        if as_dict:
            return {step.id: step for step in self.steps}
        else:
            return self.steps

    def set_data(self, data: Union[StepTextData, StepAssertData, StepGherkinData, StepRequestData, StepSleepData]):
        self.data = data

    def add_step(self, step: Type['Step']):
        self.steps.append(step)

    def set_steps(self, steps: List[Type['Step']]):
        self.steps = steps

    def add_attachment(self, attachment: Attachment):
        self.attachments.append(attachment)
