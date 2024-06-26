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

from qase.api_client_v1.models.bulk200_response import Bulk200Response

class TestBulk200Response(unittest.TestCase):
    """Bulk200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Bulk200Response:
        """Test Bulk200Response
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Bulk200Response`
        """
        model = Bulk200Response()
        if include_optional:
            return Bulk200Response(
                status = True,
                result = qase.api_client_v1.models.bulk_200_response_all_of_result.bulk_200_response_allOf_result(
                    ids = [
                        56
                        ], )
            )
        else:
            return Bulk200Response(
        )
        """

    def testBulk200Response(self):
        """Test Bulk200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
