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

from qase.api_client_v1.models.attachment_list_response import AttachmentListResponse

class TestAttachmentListResponse(unittest.TestCase):
    """AttachmentListResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AttachmentListResponse:
        """Test AttachmentListResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AttachmentListResponse`
        """
        model = AttachmentListResponse()
        if include_optional:
            return AttachmentListResponse(
                status = True,
                result = qase.api_client_v1.models.attachment_list_response_all_of_result.AttachmentListResponse_allOf_result(
                    total = 56, 
                    filtered = 56, 
                    count = 56, 
                    entities = [
                        qase.api_client_v1.models.attachment_get.AttachmentGet(
                            hash = '', 
                            file = '', 
                            mime = '', 
                            size = 56, 
                            extension = '', 
                            full_path = '', 
                            url = '', )
                        ], )
            )
        else:
            return AttachmentListResponse(
        )
        """

    def testAttachmentListResponse(self):
        """Test AttachmentListResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
