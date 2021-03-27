import pytest

import requests_mock
from apitist.constructor import converter
from requests_toolbelt.multipart import decoder
from tests.data import _attachment, _attachment_created, _list, _status_true

from qaseio.client.models import (
    AttachmentCreated,
    AttachmentInfo,
    AttachmentList,
    List,
    MimeTypes,
)


@pytest.mark.parametrize(
    "params, query",
    [
        ((10, 30), "?limit=10&offset=30"),
        ((None, 30), "?offset=30"),
        ((10, None), "?limit=10"),
    ],
)
def test_get_all_attachments(client, params, query):
    response = _status_true(_list(_attachment()))
    with requests_mock.Mocker() as m:
        m.get(client._path("attachment"), json=response)
        data = client.attachments.get_all(*params)
        assert data == converter.structure(
            response.get("result"), AttachmentList
        )
        res = client.attachments._last_res
        assert res.url == client._path("attachment" + query)


def test_get_specific_attachment(client):
    response = _status_true(_attachment())
    with requests_mock.Mocker() as m:
        m.get(client._path("attachment/1q2w3e"), json=response)
        data = client.attachments.get("1q2w3e")
        assert data == converter.structure(
            response.get("result"), AttachmentInfo
        )
        res = client.attachments._last_res
        assert res.url == client._path("attachment/1q2w3e")


def test_attachment_exists(client):
    response = _status_true(_attachment())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("attachment/1q2w3e"),
            [
                {"status_code": 200, "json": response},
                {"status_code": 404, "json": {}},
            ],
        )
        assert client.attachments.exists("1q2w3e")
        assert not client.attachments.exists("1q2w3e")


@pytest.mark.parametrize(
    "files",
    [
        (("./tests/test_data/example.json", MimeTypes.JSON, "example.json"),),
        (("./tests/test_data/example.somemime", None, "example.somemime"),),
        (
            (
                ("./tests/test_data/example.json", "text/plain"),
                MimeTypes.TXT,
                "example.json",
            ),
        ),
        (("./tests/test_data/example.png", MimeTypes.PNG, "example.png"),),
        (
            (
                (b"some content", MimeTypes.CSV, "some.csv"),
                MimeTypes.CSV,
                "some.csv",
            ),
        ),
        (
            ("./tests/test_data/example.json", MimeTypes.JSON, "example.json"),
            ("./tests/test_data/example.somemime", None, "example.somemime"),
            (
                ("./tests/test_data/example.json", "text/plain"),
                MimeTypes.TXT,
                "example.json",
            ),
            ("./tests/test_data/example.png", MimeTypes.PNG, "example.png"),
            (
                (b"some content", MimeTypes.CSV, "some.csv"),
                MimeTypes.CSV,
                "some.csv",
            ),
        ),
    ],
)
def test_upload_attachements(client, files):
    response = _status_true([_attachment_created()])
    with requests_mock.Mocker() as m:
        m.post(client._path("attachment/CODE"), json=response)
        data = client.attachments.upload(
            "CODE", *[file for file, _, _ in files]
        )
        assert data == converter.structure(
            response.get("result"), List[AttachmentCreated]
        )
        res = client.attachments._last_res
        assert res.request.body
        data = decoder.MultipartDecoder(
            res.request.body, res.request.headers["content-type"]
        )
        for i, part in enumerate(data.parts):
            file, mime, filename = files[i]
            disposition = 'form-data; name="{}"; filename="{}"'.format(
                i, filename
            )
            assert part.headers[b"content-disposition"] == disposition.encode(
                "utf-8"
            )
            if mime:
                assert part.headers[b"content-type"] == mime.encode("utf-8")
            assert part.content


def test_delete_attachment(client):
    with requests_mock.Mocker() as m:
        m.delete(client._path("attachment/1q2w3e"), json={"status": True})
        data = client.attachments.delete("1q2w3e")
        assert data is None
        res = client.attachments._last_res
        assert res.url == client._path("attachment/1q2w3e")
