import uuid

from typing import List, Optional

from .basemodel import BaseModel


class Suite(BaseModel):
    def __init__(self, title: str, description: Optional[str] = None, parent_id: Optional[str] = None):
        self.title = title
        self.description = description
        self.parent_id = parent_id
        self.id = str(uuid.uuid4())
