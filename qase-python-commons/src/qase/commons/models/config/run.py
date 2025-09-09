from typing import List, Optional
from ..basemodel import BaseModel
from ..external_link import ExternalLinkConfig
from ... import QaseUtils


class RunConfig(BaseModel):
    title: str = None
    description: str = None
    complete: bool = None
    id: int = None
    tags: List[str] = None
    external_link: Optional[ExternalLinkConfig] = None


    def __init__(self):
        self.complete = True
        self.tags = []
        self.external_link = None

    def set_title(self, title: str):
        self.title = title

    def set_description(self, description: str):
        self.description = description

    def set_complete(self, complete):
        self.complete = QaseUtils.parse_bool(complete)

    def set_id(self, id: int):
        self.id = id

    def set_tags(self, tags: List[str]):
        self.tags = tags

    def set_external_link(self, external_link: dict):
        """Set external link configuration from dictionary"""
        if external_link:
            self.external_link = ExternalLinkConfig()
            if 'type' in external_link:
                self.external_link.set_type(external_link['type'])
            if 'link' in external_link:
                self.external_link.set_link(external_link['link'])
