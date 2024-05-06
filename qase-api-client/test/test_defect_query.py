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

from qase.api_client_v1.models.defect_query import DefectQuery

class TestDefectQuery(unittest.TestCase):
    """DefectQuery unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DefectQuery:
        """Test DefectQuery
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DefectQuery`
        """
        model = DefectQuery()
        if include_optional:
            return DefectQuery(
                id = 56,
                title = '',
                actual_result = '',
                severity = '',
                status = '',
                milestone_id = 56,
                custom_fields = [
                    qase.api_client_v1.models.custom_field_value.CustomFieldValue(
                        id = 56, 
                        value = '', )
                    ],
                attachments = [
                    qase.api_client_v1.models.attachment.Attachment(
                        size = 56, 
                        mime = '', 
                        filename = '', 
                        url = '', )
                    ],
                resolved = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                member_id = 56,
                author_id = 56,
                external_data = '',
                tags = [
                    qase.api_client_v1.models.tag_value.TagValue(
                        title = '', 
                        internal_id = 56, )
                    ],
                created_at = '2021-12-30T19:23:59Z',
                updated_at = '2021-12-30T19:23:59Z'
            )
        else:
            return DefectQuery(
        )
        """

    def testDefectQuery(self):
        """Test DefectQuery"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
