import os
import uuid
import json
import pathlib

from typing import Optional, Union
from io import BytesIO, StringIO
from .basemodel import BaseModel


class Attachment(BaseModel):
    def __init__(self,
                 file_name: str,
                 mime_type: str,
                 content: Optional[str] = None,
                 file_path: Optional[str] = None,
                 temporary: bool = False):
        self.file_name = file_name
        self.mime_type = mime_type
        if (not content) and (not file_path):
            raise ValueError('Either content or file_path must be provided.')
        self.file_path = file_path
        self.content = content
        self.temporary = temporary

        if (not isinstance(content, str)) and (not isinstance(content, bytes)):
            self.content = json.dumps(self.content, default=lambda o: o.__dict__, sort_keys=False, indent=4)

        self.size = self._get_size(content)
        self.id = str(uuid.uuid4())

    def _get_size(self, content):
        if self.file_path:
            return os.path.getsize(self.file_path)
        elif content:
            return len(content)
        else:
            return 0

    def get_id(self) -> str:
        return self.id

    def get_for_upload(self) -> BytesIO:
        if self.file_path:
            with open(self.file_path, "rb") as fc:
                content = BytesIO(fc.read())
        else:
            if isinstance(self.content, str):
                content = BytesIO(bytes(self.content, 'utf-8'))
            elif isinstance(self.content, bytes):
                content = BytesIO(self.content)
        content.name = self.file_name
        content.mime = self.mime_type
        return content
