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

from qase.api_client_v1.models.external_issue import ExternalIssue

class TestExternalIssue(unittest.TestCase):
    """ExternalIssue unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ExternalIssue:
        """Test ExternalIssue
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ExternalIssue`
        """
        model = ExternalIssue()
        if include_optional:
            return ExternalIssue(
                type = '',
                issues = [
                    qase.api_client_v1.models.external_issue_issues_inner.ExternalIssue_issues_inner(
                        id = '', 
                        link = '', )
                    ]
            )
        else:
            return ExternalIssue(
        )
        """

    def testExternalIssue(self):
        """Test ExternalIssue"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
