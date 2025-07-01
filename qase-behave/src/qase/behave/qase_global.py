import os
import mimetypes
import logging
from typing import Optional, Union
from qase.commons.models import Attachment

logger = logging.getLogger(__name__)


class QaseGlobal:
    """
    Global Qase object for behave integration.
    Provides attachment functionality for test scenarios.
    """
    
    def __init__(self):
        self._current_scenario = None
    
    def _set_current_scenario(self, scenario):
        """Set the current scenario for attachment tracking"""
        self._current_scenario = scenario
    
    def attach(self, 
               file_path: Optional[str] = None,
               content: Optional[Union[str, bytes]] = None,
               file_name: Optional[str] = None,
               mime_type: Optional[str] = None) -> None:
        """
        Attach a file or content to the current test scenario.
        
        Args:
            file_path: Path to the file to attach
            content: Content to attach (string or bytes)
            file_name: Name for the attachment (if not provided, will be derived from file_path)
            mime_type: MIME type of the attachment (if not provided, will be auto-detected)
        """
        
        if self._current_scenario is None:
            raise RuntimeError("No active scenario. Cannot attach file.")
        
        if file_path and content:
            raise ValueError("Either file_path or content must be provided, not both.")
        
        if not file_path and not content:
            raise ValueError("Either file_path or content must be provided.")
        
        # Determine file name
        if file_name is None:
            if file_path:
                file_name = os.path.basename(file_path)
            else:
                file_name = "attachment.txt"
        
        # Determine MIME type
        if mime_type is None:
            if file_path:
                mime_type, _ = mimetypes.guess_type(file_path)
            elif file_name:
                mime_type, _ = mimetypes.guess_type(file_name)
            elif isinstance(content, bytes):
                mime_type = "application/octet-stream"
            else:
                mime_type = "text/plain"
            
            if mime_type is None:
                mime_type = "application/octet-stream"
        
        # Create attachment
        if file_path:
            attachment = Attachment(
                file_name=file_name,
                mime_type=mime_type,
                file_path=file_path
            )
        else:
            attachment = Attachment(
                file_name=file_name,
                mime_type=mime_type,
                content=content
            )
        
        # Add attachment to current scenario
        if not hasattr(self._current_scenario, 'attachments'):
            self._current_scenario.attachments = []
        
        self._current_scenario.attachments.append(attachment)


    def comment(self, message: str) -> None:
        """
        Add a comment to the current test scenario.
        
        This method allows you to add comments that will be included in the test result.
        Comments are useful for providing additional context about test execution,
        debugging information, or any other relevant notes.
        
        Args:
            message: The comment message to add to the scenario
            
        Raises:
            RuntimeError: If no active scenario is available
            
        Example:
            >>> qase.comment("Test completed successfully")
            >>> qase.comment("Debug info: user logged in")
        """
        if self._current_scenario is None:
            raise RuntimeError("No active scenario. Cannot add comment.")
            
        # If this is the first comment or message is None, set it directly
        if not hasattr(self._current_scenario, 'message') or self._current_scenario.message is None:
            self._current_scenario.message = message
        else:
            # If message already exists, append the new comment
            self._current_scenario.message = self._current_scenario.message + '\n' + message    

# Global instance
qase = QaseGlobal() 
