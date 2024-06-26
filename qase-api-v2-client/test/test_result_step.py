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

from qase.api_client_v2.models.result_step import ResultStep

class TestResultStep(unittest.TestCase):
    """ResultStep unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ResultStep:
        """Test ResultStep
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ResultStep`
        """
        model = ResultStep()
        if include_optional:
            return ResultStep(
                data = qase.models.result_step_data.ResultStepData(
                    action = '', 
                    expected_result = '', 
                    input_data = '', 
                    attachments = [
                        ''
                        ], ),
                execution = qase.models.result_step_execution.ResultStepExecution(
                    start_time = 1.337, 
                    end_time = 1.337, 
                    status = 'passed', 
                    duration = 56, 
                    comment = '', 
                    attachments = [
                        ''
                        ], ),
                steps = [
                    None
                    ]
            )
        else:
            return ResultStep(
        )
        """

    def testResultStep(self):
        """Test ResultStep"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
