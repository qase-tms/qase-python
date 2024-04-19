from .step import Step, StepTextData
from .attachment import Attachment


class QaseRuntimeException(Exception):
    pass


class Runtime:
    def __init__(self):
        self.result = None
        self.steps = {}
        self.step_id = None

    def add_step(self, step: Step):
        try:
            if self.step_id:
                step.set_parent_id(self.step_id)

            self.steps[step.id] = step
            self.step_id = step.id
        except Exception as e:
            raise QaseRuntimeException(e)

    def finish_step(self, id: str, status: str, data=None):
        try:
            self.steps[id].execution.set_status(status)
            if data:
                self.steps[id].set_data(data)

            self.steps[id].execution.complete()
            self.step_id = self.steps[id].parent_id
        except Exception as e:
            raise QaseRuntimeException(e)

    def add_attachment(self, attachment: Attachment):
        try:
            if self.step_id:
                self.steps[self.step_id].add_attachment(attachment)
            else:
                self.result.add_attachment(attachment)
        except Exception as e:
            raise QaseRuntimeException(e)
