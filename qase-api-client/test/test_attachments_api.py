# coding: utf-8

"""
    Qase.io TestOps API v1

    Qase TestOps API v1 Specification.

    The version of the OpenAPI document: 1.0.0
    Contact: support@qase.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from qase.api_client_v1.api.attachments_api import AttachmentsApi


class TestAttachmentsApi(unittest.TestCase):
    """AttachmentsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = AttachmentsApi()

    def tearDown(self) -> None:
        pass

    def test_delete_attachment(self) -> None:
        """Test case for delete_attachment

        Remove attachment by Hash
        """
        pass

    def test_get_attachment(self) -> None:
        """Test case for get_attachment

        Get attachment by Hash
        """
        pass

    def test_get_attachments(self) -> None:
        """Test case for get_attachments

        Get all attachments
        """
        pass

    def test_upload_attachment(self) -> None:
        """Test case for upload_attachment

        Upload attachment
        """
        pass


if __name__ == '__main__':
    unittest.main()
