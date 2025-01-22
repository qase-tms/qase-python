from typing import Union, Tuple
from qase.commons import QaseUtils
import mimetypes
from qase.commons.models.attachment import Attachment

from .plugin import QaseRuntimeSingleton


class qase:
    """Class with decorators for robotframework"""

    @staticmethod
    def attach(
            *files: Union[str, Tuple[str, str], Tuple[bytes, str, str]]
    ):
        """
                Attach files to test results

                `files` could be:
                    - str - only `filepath`
                    - str, str - `filepath` and `mime-type` for it
                    - bytes, str, str - `source` data, `mime-type` and `filename`

                >>> from src.client.models import MimeTypes
                ... qase.attach(
                ...     (driver.get_screenshot_as_png(), MimeTypes.PNG, "page.png")
                ... )
                """
        for file in files:
            filename = None
            content = None
            file_path = None

            if isinstance(file, tuple):
                if len(file) == 2:
                    file_path, mime = file
                    filename = QaseUtils.get_filename(file_path)
                else:
                    content, mime, filename = file
            elif isinstance(file, str):
                file_path = file
                mime = mimetypes.guess_type(file)[0]
                filename = QaseUtils.get_filename(file_path)

            attachment = Attachment(file_name=filename, content=content, mime_type=mime, file_path=file_path)
            QaseRuntimeSingleton.get_instance().add_attachment(attachment)
