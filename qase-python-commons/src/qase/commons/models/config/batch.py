from ..basemodel import BaseModel


class BatchConfig(BaseModel):
    size: int = None

    def __init__(self):
        self.size = 200

    def set_size(self, size: int):
        if size > 2000 or size == 0:
            raise ValueError("Batch size should be greater than 0 and less than 2000")
        self.size = size
