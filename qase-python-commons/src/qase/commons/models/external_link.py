from enum import Enum
from typing import Optional
from .basemodel import BaseModel


class ExternalLinkType(Enum):
    """External link types supported by Qase TestOps"""
    JIRA_CLOUD = 'jiraCloud'
    JIRA_SERVER = 'jiraServer'


class ExternalLinkConfig(BaseModel):
    """Configuration for external link"""
    type: ExternalLinkType = None
    link: str = None

    def __init__(self, type: ExternalLinkType = None, link: str = None):
        self.type = type
        self.link = link

    def set_type(self, type: str):
        """Set external link type from string"""
        if type == 'jiraCloud':
            self.type = ExternalLinkType.JIRA_CLOUD
        elif type == 'jiraServer':
            self.type = ExternalLinkType.JIRA_SERVER
        else:
            raise ValueError(f"Invalid external link type: {type}. Supported types: jiraCloud, jiraServer")

    def set_link(self, link: str):
        """Set external link URL or identifier"""
        self.link = link

    def to_api_type(self) -> str:
        """Convert to API enum value"""
        if self.type == ExternalLinkType.JIRA_CLOUD:
            return 'jira-cloud'
        elif self.type == ExternalLinkType.JIRA_SERVER:
            return 'jira-server'
        else:
            raise ValueError(f"Invalid external link type: {self.type}")
