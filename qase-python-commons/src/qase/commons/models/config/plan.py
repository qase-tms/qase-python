from ..basemodel import BaseModel


class PlanConfig(BaseModel):
    id: int = None

    def set_id(self, id: int):
        self.id = id
