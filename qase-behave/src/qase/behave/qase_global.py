import os
import mimetypes
import logging
from typing import Optional, Union, Dict
from qase.commons.models import Attachment

logger = logging.getLogger(__name__)


class QaseGlobal:
    """
    Global Qase object for behave integration.
    Provides attachment functionality for test scenarios.
    """
    
    def __init__(self):
        self._current_scenario = None
        self._current_step = None
        self._pending_step_attachments: Dict[str, list] = {}
    
    def _set_current_scenario(self, scenario):
        """Set the current scenario for attachment tracking"""
        self._current_scenario = scenario
        # Clear pending attachments when scenario changes
        self._pending_step_attachments.clear()
    
    def _set_current_step(self, step):
        """Set the current step for attachment tracking"""
        self._current_step = step
        # If step is set, apply any pending attachments
        if step is not None:
            step_id = step.id
            if step_id in self._pending_step_attachments:
                for attachment in self._pending_step_attachments[step_id]:
                    step.add_attachment(attachment)
                del self._pending_step_attachments[step_id]
            # Also apply attachments stored for the next step
            if '_next_step' in self._pending_step_attachments:
                for attachment in self._pending_step_attachments['_next_step']:
                    step.add_attachment(attachment)
                del self._pending_step_attachments['_next_step']
    
    def _create_attachment(self,
                           file_path: Optional[str] = None,
                           content: Optional[Union[str, bytes]] = None,
                           file_name: Optional[str] = None,
                           mime_type: Optional[str] = None) -> Attachment:
        """
        Create an Attachment object from the provided parameters.
        
        Args:
            file_path: Path to the file to attach
            content: Content to attach (string or bytes)
            file_name: Name for the attachment (if not provided, will be derived from file_path)
            mime_type: MIME type of the attachment (if not provided, will be auto-detected)
            
        Returns:
            Attachment object
            
        Raises:
            ValueError: If both file_path and content are provided, or if neither is provided
        """
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
            return Attachment(
                file_name=file_name,
                mime_type=mime_type,
                file_path=file_path
            )
        else:
            return Attachment(
                file_name=file_name,
                mime_type=mime_type,
                content=content
            )
    
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
        
        attachment = self._create_attachment(file_path, content, file_name, mime_type)
        
        # Add attachment to current scenario
        if not hasattr(self._current_scenario, 'attachments'):
            self._current_scenario.attachments = []
        
        self._current_scenario.attachments.append(attachment)

    def attach_to_step(self, 
                       file_path: Optional[str] = None,
                       content: Optional[Union[str, bytes]] = None,
                       file_name: Optional[str] = None,
                       mime_type: Optional[str] = None) -> None:
        """
        Attach a file or content to the current test step.
        If the step is not yet available, the attachment will be stored
        and applied when the step is created.
        
        Args:
            file_path: Path to the file to attach
            content: Content to attach (string or bytes)
            file_name: Name for the attachment (if not provided, will be derived from file_path)
            mime_type: MIME type of the attachment (if not provided, will be auto-detected)
            
        Raises:
            RuntimeError: If no active scenario is available
        """
        
        if self._current_scenario is None:
            raise RuntimeError("No active scenario. Cannot attach file to step.")
        
        attachment = self._create_attachment(file_path, content, file_name, mime_type)
        
        # Add attachment to current step if available, otherwise store for later
        if self._current_step is not None:
            self._current_step.add_attachment(attachment)
        else:
            # Store attachment to be applied when step is created
            # Use a temporary key that will be matched when step is set
            # We'll use the step's line number or name as identifier
            # For now, use a special key that will be applied to the next step
            if '_next_step' not in self._pending_step_attachments:
                self._pending_step_attachments['_next_step'] = []
            self._pending_step_attachments['_next_step'].append(attachment)


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
