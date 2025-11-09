from typing import Union

from ..basemodel import BaseModel


class BatchConfig(BaseModel):
    size: int

    def __init__(self):
        self.size = 200

    def set_size(self, size: Union[int, str]):
        try:
            if isinstance(size, str):
                size = size.strip()
                size_int = int(size)
            else:
                size_int = size
            if size_int > 2000 or size_int == 0:
                self.size = size_int
        except ValueError:
            raise ValueError("Batch size should be numeric value")
