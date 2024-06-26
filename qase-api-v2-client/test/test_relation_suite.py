# coding: utf-8

"""
    Qase.io TestOps API v2

    Qase TestOps API v2 Specification.

    The version of the OpenAPI document: 2.0.0
    Contact: support@qase.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from qase.api_client_v2.models.relation_suite import RelationSuite

class TestRelationSuite(unittest.TestCase):
    """RelationSuite unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RelationSuite:
        """Test RelationSuite
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RelationSuite`
        """
        model = RelationSuite()
        if include_optional:
            return RelationSuite(
                data = [
                    qase.models.relation_suite_item.RelationSuiteItem(
                        title = '', 
                        public_id = 56, )
                    ]
            )
        else:
            return RelationSuite(
                data = [
                    qase.models.relation_suite_item.RelationSuiteItem(
                        title = '', 
                        public_id = 56, )
                    ],
        )
        """

    def testRelationSuite(self):
        """Test RelationSuite"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
