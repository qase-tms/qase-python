from typing import Optional, Union, Dict, List, Type
import time
import uuid
from qaseio.commons.models.attachment import Attachment

class StepTextData(object):
    def __init__(self, action: str, expected_result: Optional[str] = None):
        self.action = action
        self.expected_result = expected_result

class StepAssertData(object):
    def __init__(self, expected: str, actual: str, message: str):
        self.expected = expected
        self.actual = actual
        self.message = message

class StepGherkinData(object):
    def __init__(self, keyword: str, name: str, line: int):
        self.keyword = keyword
        self.name = name
        self.line = line

class StepRequestData(object):
    def __init__(self, request_body: str, request_headers: Dict[str, str], request_method: str, request_url: str):
        if (isinstance(request_body, bytes)):
            request_body = request_body.decode('utf-8')
        self.request_body = request_body
        if (isinstance(request_headers, bytes)):
            request_headers = request_headers.decode('utf-8')
        self.request_headers = request_headers
        self.request_method = request_method
        self.request_url = request_url

    def add_response(self, status_code: int, response_body: Optional[str] = None, response_headers: Optional[Dict[str, str]] = None):
        self.status_code = status_code

        if (isinstance(response_body, bytes)):
            response_body = response_body.decode('utf-8')
        self.response_body = response_body
        if (isinstance(response_headers, bytes)):
            response_headers = response_headers.decode('utf-8')
        self.response_headers = response_headers

class StepDbQueryData(object):
    def __init__(self, query: str, expected_result: str):
        self.query = query

class StepSleepData(object):
    def __init__(self, duration: int):
        self.duration = duration

class StepExecution(object):
    def __init__(self, status: Optional[str] = 'untested', end_time: int = 0, duration: int = 0):
        self.start_time = time.time()
        self.status = status
        self.end_time = end_time
        self.duration = duration

    def set_status(self, status: Optional[str]):
        if (status in ['passed', 'failed', 'skipped', 'untested']):
            self.status = status
        else:
            raise ValueError('Step status must be one of: passed, failed, skipped, untested')
        
    def complete(self):
        self.end_time = time.time()
        self.duration = int((self.end_time - self.start_time) * 1000)

class Step(object):
    def __init__(self, 
        step_type: str, 
        id: Optional[str], 
        data: Optional[Union[StepTextData, StepAssertData, StepGherkinData, StepRequestData]] = None, 
        parent_id: Optional[str] = None
    ):
        if (id):
            self.id = id
        else:
            self.id = str(uuid.uuid4())

        if (step_type in ['text', 'assert', 'gherkin', 'request']):
            self.step_type = step_type
        else:
            raise ValueError('Step type must be one of: text, assert, gherkin, request')
        
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
        if (as_dict):
            return {step.id: step for step in self.steps}
        else:
            return self.steps

    def set_data(self, data: Union[StepTextData, StepAssertData, StepGherkinData, StepRequestData]):
        self.data = data

    def add_step(self, step: Type['Step']):
        self.steps.append(step)

    def set_steps(self, steps: List[Type['Step']]):
        self.steps = steps

    def add_attachment(self, attachment: Attachment):
        self.attachments.append(attachment)