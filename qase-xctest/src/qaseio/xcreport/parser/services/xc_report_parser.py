import json
import subprocess
from typing import Type, TypeVar

import attr

from qaseio.xcreport.parser import models as m

T = TypeVar("T")


@attr.s
class XCReportParser:
    xc_path: str = attr.ib()

    def open_report_object(self) -> m.ActionsInvocationRecord:
        return self.__open_object(m.ActionsInvocationRecord)

    def open_attachment(self, idFile=None):
        prams = [
            "xcrun",
            "xcresulttool",
            "get",
            "--path",
            self.xc_path,
            "--format",
            "raw",
        ]
        if idFile is not None:
            prams.extend(["--id", idFile])

        result = subprocess.run(prams, stdout=subprocess.PIPE)
        return result.stdout

    def extract_attachment_from_activity_summary(
        self, activity_summary: m.ActionTestActivitySummary, attachment_name
    ):
        if (
            activity_summary.activity_type
            == m.ActivityType.ATTACHMENT_CONTAINER
        ):
            for attachment in activity_summary.attachments:
                if (
                    attachment.name == attachment_name
                    and attachment.payload_ref is not None
                ):
                    binary_data = self.open_attachment(
                        attachment.payload_ref.obj_id
                    )
                    return binary_data

    def extract_tests(
        self, report: m.ActionsInvocationRecord
    ) -> [m.ActionTestSummary]:
        for action_record in report.actions:
            tests_ref = action_record.action_result.tests_ref
            if tests_ref is not None:
                test_plan_run_summaries = self.__open_object(
                    m.ActionTestPlanRunSummaries, tests_ref.obj_id
                )
                for test_plan_run_summary in test_plan_run_summaries.summaries:
                    for (
                        testable_summary
                    ) in test_plan_run_summary.testable_summaries:
                        for test_identifiable_object in testable_summary.tests:
                            return self.__extract_identifiable_object(
                                test_identifiable_object
                            )

    def __extract_identifiable_object(
        self, test_identifiable_object: m.ActionTestSummaryIdentifiableObject
    ) -> [m.ActionTestSummary]:
        if isinstance(test_identifiable_object, m.ActionTestSummaryGroup):
            test_summary_group: m.ActionTestSummaryGroup = (
                test_identifiable_object
            )
            tests = []
            for test in test_summary_group.subtests:
                tests.extend(self.__extract_identifiable_object(test))
            return tests
        elif isinstance(test_identifiable_object, m.ActionTestMetadata):
            test_metadata: m.ActionTestMetadata = test_identifiable_object
            if test_metadata.summary_ref is not None:
                return [
                    self.__open_object(
                        m.ActionTestSummary, test_metadata.summary_ref.obj_id
                    )
                ]
            else:
                return []
        elif isinstance(test_identifiable_object, m.ActionTestSummary):
            return [test_identifiable_object]
        else:
            return []

    def __open_object(self, to_type: Type[T], file_id: str = None) -> T:
        return to_type.from_report(self.__open_json(file_id))

    def __open_json(self, file_id: str = None):
        prams = [
            "xcrun",
            "xcresulttool",
            "get",
            "--path",
            self.xc_path,
            "--format",
            "json",
        ]
        if file_id is not None:
            prams.extend(["--id", file_id])

        result = subprocess.run(
            prams, stdout=subprocess.PIPE, encoding="utf-8"
        )
        parsed_json = json.loads(result.stdout)
        return parsed_json
