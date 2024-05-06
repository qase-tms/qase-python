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

from qase.api_client_v1.models.project_response import ProjectResponse

class TestProjectResponse(unittest.TestCase):
    """ProjectResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ProjectResponse:
        """Test ProjectResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ProjectResponse`
        """
        model = ProjectResponse()
        if include_optional:
            return ProjectResponse(
                status = True,
                result = qase.api_client_v1.models.project.Project(
                    title = '', 
                    code = '', 
                    counts = qase.api_client_v1.models.project_counts.Project_counts(
                        cases = 56, 
                        suites = 56, 
                        milestones = 56, 
                        runs = qase.api_client_v1.models.project_counts_runs.Project_counts_runs(
                            total = 56, 
                            active = 56, ), 
                        defects = qase.api_client_v1.models.project_counts_defects.Project_counts_defects(
                            total = 56, 
                            open = 56, ), ), )
            )
        else:
            return ProjectResponse(
        )
        """

    def testProjectResponse(self):
        """Test ProjectResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
