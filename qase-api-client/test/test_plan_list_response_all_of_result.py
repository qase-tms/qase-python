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

from src.qase.api_client_v1.models.plan_list_response_all_of_result import PlanListResponseAllOfResult

class TestPlanListResponseAllOfResult(unittest.TestCase):
    """PlanListResponseAllOfResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PlanListResponseAllOfResult:
        """Test PlanListResponseAllOfResult
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PlanListResponseAllOfResult`
        """
        model = PlanListResponseAllOfResult()
        if include_optional:
            return PlanListResponseAllOfResult(
                total = 56,
                filtered = 56,
                count = 56,
                entities = [
                    src.qase.api_client_v1.models.plan.Plan(
                        id = 56, 
                        title = '', 
                        description = '', 
                        cases_count = 56, 
                        created_at = '2021-12-30T19:23:59Z', 
                        updated_at = '2021-12-30T19:23:59Z', 
                        created = '2021-12-30 19:23:59', 
                        updated = '2021-12-30 19:23:59', )
                    ]
            )
        else:
            return PlanListResponseAllOfResult(
        )
        """

    def testPlanListResponseAllOfResult(self):
        """Test PlanListResponseAllOfResult"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
