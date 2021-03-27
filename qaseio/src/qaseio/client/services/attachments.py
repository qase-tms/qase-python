import mimetypes
import ntpath
from typing import List, Tuple, Union

from qaseio.client.models import (
    AttachmentCreated,
    AttachmentInfo,
    AttachmentList,
)
from qaseio.client.services import BaseService, NotFoundException


class Attachments(BaseService):
    def get_all(self, limit=None, offset=None):
        return self.vr(
            self.s.get(
                self.path("attachment"),
                params={"limit": limit, "offset": offset},
            ),
            to_type=AttachmentList,
        )

    def get(self, hash: str):
        return self.vr(
            self.s.get(self.path("attachment/{}".format(hash))),
            to_type=AttachmentInfo,
        )

    def upload(
        self,
        code: str,
        *file_infos: Union[str, Tuple[str, str], Tuple[bytes, str, str]],
    ):
        files = []
        for _id, file in enumerate(file_infos):
            filename = None
            if isinstance(file, tuple):
                if len(file) == 2:
                    path, mime = file
                else:
                    path, mime, filename = file
            else:
                path = file
                mime = mimetypes.guess_type(file)[0]
            if isinstance(path, bytes):
                content = path
            else:
                content = open(path, "rb")
            files.append(
                (str(_id), (filename or ntpath.basename(path), content, mime))
            )

        return self.vr(
            self.s.post(self.path("attachment/{}".format(code)), files=files),
            to_type=List[AttachmentCreated],
        )

    def delete(self, hash: str):
        return self.vr(
            self.s.delete(self.path("attachment/{}".format(hash))),
            to_type=None,
        )

    def exists(self, code: str):
        try:
            return self.get(code)
        except NotFoundException:
            return False
