import os
import uuid
from typing import Optional
from io import BytesIO, StringIO
import json

class Attachment:
    def __init__(self, 
                 file_name: str,
                 mime_type: str,
                 content: Optional[str] = None,
                 file_path: Optional[str] = None,
                 temporary: bool = False):
        # File name of the attachment
        self.file_name = file_name

        # Mime type of the attachment
        self.mime_type = mime_type

        if (not content) and (not file_path):
            raise ValueError('Either content or file_path must be provided.')
        
        # File path to the attachment
        self.file_path = file_path

        # String content of the attachment
        self.content = content

        # Temporary is used to indicate that the attachment should be used for result only
        self.temporary = temporary

        if (not isinstance(content, str)) and (not isinstance(content, bytes)):
            self.content = json.dumps(self.content, default=lambda o: o.__dict__, sort_keys=False, indent=4)

        self.size = self._get_size(content)
        self.id = str(uuid.uuid4())
        
    # Returns size of the attachment
    def _get_size(self, content) -> int:
        if self.file_path:
            return os.path.getsize(self.file_path)
        elif content:
            return len(content)
        else:
            return 0
        
    def get_id(self):
        return self.id
    
    # Returns content for upload
    def get_for_upload(self) -> BytesIO:
        if self.file_path:
            content = open(self.file_path, "rb")
        else:
            if isinstance(self.content, str):
                content = StringIO(self.content)
            elif isinstance(self.content, bytes):
                content = BytesIO(self.content)
            content.name = self.file_name
        content.mime = self.mime_type
        return content
