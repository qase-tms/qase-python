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

from qase.api_client_v1.models.run_stats import RunStats

class TestRunStats(unittest.TestCase):
    """RunStats unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RunStats:
        """Test RunStats
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RunStats`
        """
        model = RunStats()
        if include_optional:
            return RunStats(
                total = 56,
                statuses = {
                    'key' : 56
                    },
                untested = 56,
                passed = 56,
                failed = 56,
                blocked = 56,
                skipped = 56,
                retest = 56,
                in_progress = 56,
                invalid = 56
            )
        else:
            return RunStats(
        )
        """

    def testRunStats(self):
        """Test RunStats"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
