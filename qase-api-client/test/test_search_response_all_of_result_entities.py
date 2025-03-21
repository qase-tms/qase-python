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

from qase.api_client_v1.models.search_response_all_of_result_entities import SearchResponseAllOfResultEntities

class TestSearchResponseAllOfResultEntities(unittest.TestCase):
    """SearchResponseAllOfResultEntities unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SearchResponseAllOfResultEntities:
        """Test SearchResponseAllOfResultEntities
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SearchResponseAllOfResultEntities`
        """
        model = SearchResponseAllOfResultEntities()
        if include_optional:
            return SearchResponseAllOfResultEntities(
                id = 56,
                run_id = 56,
                title = '',
                description = '',
                status = '',
                status_text = '',
                start_time = '2021-12-30T19:23:59Z',
                end_time = '2021-12-30T19:23:59Z',
                public = True,
                stats = qase.api_client_v1.models.run_stats.Run_stats(
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
                    invalid = 56, ),
                time_spent = 56,
                environment = qase.api_client_v1.models.run_environment.Run_environment(
                    title = '', 
                    description = '', 
                    slug = '', 
                    host = '', ),
                milestone = qase.api_client_v1.models.run_milestone.Run_milestone(
                    title = '', 
                    description = '', ),
                custom_fields = [
                    qase.api_client_v1.models.custom_field_value.CustomFieldValue(
                        id = 56, 
                        value = '', )
                    ],
                tags = [
                    qase.api_client_v1.models.tag_value.TagValue(
                        title = '', 
                        internal_id = 56, )
                    ],
                cases = [
                    56
                    ],
                plan_id = 56,
                hash = '',
                result_hash = '',
                comment = '',
                stacktrace = '',
                case_id = 56,
                steps = [
                    qase.api_client_v1.models.test_step.TestStep(
                        hash = '', 
                        shared_step_hash = '', 
                        shared_step_nested_hash = '', 
                        position = 56, 
                        action = '', 
                        expected_result = '', 
                        data = '', 
                        attachments = [
                            qase.api_client_v1.models.attachment.Attachment(
                                size = 56, 
                                mime = '', 
                                filename = '', 
                                url = '', )
                            ], )
                    ],
                is_api_result = True,
                time_spent_ms = 56,
                attachments = [
                    qase.api_client_v1.models.attachment.Attachment(
                        size = 56, 
                        mime = '', 
                        filename = '', 
                        url = '', )
                    ],
                requirement_id = 56,
                parent_id = 56,
                member_id = 56,
                type = 56,
                created_at = '2021-12-30T19:23:59Z',
                updated_at = '2021-12-30T19:23:59Z',
                test_case_id = 56,
                position = 56,
                preconditions = '',
                postconditions = '',
                severity = '',
                priority = 56,
                layer = 56,
                is_flaky = 56,
                behavior = 56,
                automation = 56,
                milestone_id = 56,
                suite_id = 56,
                steps_type = '',
                params = None,
                author_id = 56,
                defect_id = 56,
                actual_result = '',
                resolved = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                external_data = '',
                cases_count = 56
            )
        else:
            return SearchResponseAllOfResultEntities(
                run_id = 56,
                plan_id = 56,
                result_hash = '',
                requirement_id = 56,
                test_case_id = 56,
                defect_id = 56,
        )
        """

    def testSearchResponseAllOfResultEntities(self):
        """Test SearchResponseAllOfResultEntities"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
