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

from src.qase.api_client_v1.models.custom_field_create import CustomFieldCreate

class TestCustomFieldCreate(unittest.TestCase):
    """CustomFieldCreate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CustomFieldCreate:
        """Test CustomFieldCreate
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CustomFieldCreate`
        """
        model = CustomFieldCreate()
        if include_optional:
            return CustomFieldCreate(
                title = '',
                value = [
                    src.qase.api_client_v1.models.custom_field_create_value_inner.CustomFieldCreate_value_inner(
                        id = 56, 
                        title = '', )
                    ],
                entity = 0,
                type = 0,
                placeholder = '',
                default_value = '',
                is_filterable = True,
                is_visible = True,
                is_required = True,
                is_enabled_for_all_projects = True,
                projects_codes = [
                    ''
                    ]
            )
        else:
            return CustomFieldCreate(
                title = '',
                entity = 0,
                type = 0,
        )
        """

    def testCustomFieldCreate(self):
        """Test CustomFieldCreate"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
