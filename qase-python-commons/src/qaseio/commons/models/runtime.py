from qaseio.commons.models.step import Step, StepTextData
from qaseio.commons.models.attachment import Attachment

class Runtime:
    def __init__(self):
        self.result = None
        self.steps = {}
        self.step_id = None

    def add_step(self, step: Step):
        if self.step_id:
            step.set_parent_id(self.step_id)

        self.steps[step.id] = step
        self.step_id = step.id

    def finish_step(self, id:str, status:str, data = None):
        self.steps[id].execution.set_status(status)
        if (data):
            self.steps[id].set_data(data)

        self.steps[id].execution.complete()
        self.step_id = self.steps[id].parent_id

    def add_attachment(self, attachment: Attachment):
        if self.step_id:
            self.steps[self.step_id].add_attachment(attachment)
        else:
            self.result.add_attachment(attachment)