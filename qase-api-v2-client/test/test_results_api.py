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

from src.qase.api_client_v2.api import ResultsApi


class TestResultsApi(unittest.TestCase):
    """ResultsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = ResultsApi()

    def tearDown(self) -> None:
        pass

    def test_create_result_v2(self) -> None:
        """Test case for create_result_v2

        (Beta) Create test run result
        """
        pass

    def test_create_results_v2(self) -> None:
        """Test case for create_results_v2

        (Beta) Bulk create test run result
        """
        pass


if __name__ == '__main__':
    unittest.main()
