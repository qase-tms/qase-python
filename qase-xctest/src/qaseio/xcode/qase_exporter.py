import json
from typing import List, Optional, Tuple

import attr

from qaseio.client import QaseApi
from qaseio.client.models import (
    AttachmentCreated,
    MimeTypes,
    TestRunCreate,
    TestRunResultCreate,
    TestRunResultStatus,
    TestRunResultStepCreate,
)
from qaseio.client.services import BadRequestException
from qaseio.xcreport import parser as p

ACTION_TEST_SUMMARY_TO_QASE_STATUS = {
    p.TestStatus.FAULURE: TestRunResultStatus.FAILED,
    p.TestStatus.UNDEFINE: TestRunResultStatus.FAILED,
    p.TestStatus.SUCCESS: TestRunResultStatus.PASSED,
}

ATTACHMENT_TYPES = {p.UniformTypeIdentifier.PNG: MimeTypes.PNG}


QASE_STEP_MARKER_FILE = "Qase step marker"
QASE_CONFIG_FILE = "Qase config"


@attr.s
class QaseExtractor:
    xc_paths: List[str] = attr.ib()
    api_token: str = attr.ib()
    project_code: str = attr.ib()
    upload_attachments: bool = attr.ib(default=True)
    test_run_name: str = attr.ib(default="Run")

    def __attrs_post_init__(self):
        self._ignored_attachment_names = [
            QASE_STEP_MARKER_FILE,
            QASE_CONFIG_FILE,
        ]

    def process(self):

        tests_with_qase: List[
            Tuple[int, p.ActionTestSummary, p.XCReportParser]
        ] = []
        qase_ids: List[int] = []

        for xc_path in self.xc_paths:
            parser = p.XCReportParser(xc_path)
            report = parser.open_report_object()
            tests = parser.extract_tests(report)

            for test in tests:
                case_id = self.__find_case_id(parser, test)
                if case_id is None:
                    continue
                tests_with_qase.append((int(case_id), test, parser))
                if case_id in qase_ids:
                    continue
                qase_ids.append(int(case_id))

        qase = QaseApi(self.api_token)

        test_run = qase.runs.create(
            self.project_code, TestRunCreate(self.test_run_name, qase_ids)
        )

        for case_id, test, parser in tests_with_qase:
            steps: List[TestRunResultStepCreate] = []
            # Find steps
            position = 1
            test_run_attachments: List[str] = []
            for activity_summary in test.activity_summaries:
                attachments = (
                    self.__upload_attachments(parser, activity_summary, qase)
                    if self.upload_attachments
                    else []
                )
                if not self.__contains_step_mark(parser, activity_summary):
                    test_run_attachments.extend(attachments)
                    continue
                # Prepare step
                contains_failure = self.__activity_summary_contains_type(
                    activity_summary, p.ActivityType.FAILURE
                )
                steps.append(
                    TestRunResultStepCreate(
                        position,
                        TestRunResultStatus.FAILED
                        if contains_failure
                        else TestRunResultStatus.PASSED,
                        attachments,
                        self.__create_comment(activity_summary),
                    )
                )
                position += 1

            # Create test result
            try:
                qase.results.create(
                    self.project_code,
                    test_run.id,
                    TestRunResultCreate(
                        case_id,
                        ACTION_TEST_SUMMARY_TO_QASE_STATUS[test.test_status],
                        int(test.duration),
                        steps=steps,
                        attachments=test_run_attachments,
                    ),
                )
            except BadRequestException:
                try:
                    # Try without steps
                    qase.results.create(
                        self.project_code,
                        test_run.id,
                        TestRunResultCreate(
                            case_id,
                            ACTION_TEST_SUMMARY_TO_QASE_STATUS[
                                test.test_status
                            ],
                            int(test.duration),
                            comment="Check number of steps in your code. "
                            "They are not equally.",
                            attachments=test_run_attachments,
                        ),
                    )
                    print(
                        "Check number of steps in your code. "
                        "They are not equally. case_id:",
                        case_id,
                    )
                except Exception as err:
                    print("case_id:", case_id, "error:", err)
            except Exception as err:
                print("case_id:", case_id, "error:", err)

    def __extract_qase_config(
        self, parser: p.XCReportParser, test_summary: p.ActionTestSummary
    ):
        for activity_summary in test_summary.activity_summaries:
            binary_data = parser.extract_attachment_from_activity_summary(
                activity_summary, QASE_CONFIG_FILE
            )
            if binary_data is not None:
                config = json.loads(binary_data)
                return config

    def __activity_is_step_mark(
        self,
        parser: p.XCReportParser,
        activity_summary: p.ActionTestActivitySummary,
    ):
        mark = parser.extract_attachment_from_activity_summary(
            activity_summary, QASE_STEP_MARKER_FILE
        )
        return mark is not None

    def __contains_step_mark(
        self,
        parser: p.XCReportParser,
        activity_summary: p.ActionTestActivitySummary,
    ):
        for sub_activity_summary in activity_summary.subactivities:
            if self.__activity_is_step_mark(parser, sub_activity_summary):
                return True
        return False

    def __activity_summary_contains_type(
        self,
        activity_summary: p.ActionTestActivitySummary,
        act_type: p.ActivityType,
    ):
        if activity_summary.activity_type == act_type:
            return True
        else:
            for subactivity in activity_summary.subactivities:
                return self.__activity_summary_contains_type(
                    subactivity, act_type
                )

        return False

    def __find_all_attachments(
        self, summary: p.ActionTestActivitySummary
    ) -> List[p.ActionTestAttachment]:
        result: List[p.ActionTestAttachment] = []
        filtered = list(
            filter(
                lambda a: a.name not in self._ignored_attachment_names
                and a.payload_ref is not None,
                summary.attachments,
            )
        )
        result.extend(filtered)
        for sub in summary.subactivities:
            subResult = self.__find_all_attachments(sub)
            result.extend(subResult)
        return result

    def __find_case_id(
        self, parser: p.XCReportParser, test_summary: p.ActionTestSummary
    ) -> Optional[str]:
        test_config = self.__extract_qase_config(parser, test_summary)
        if test_config is None:
            return None
        return test_config["caseId"]

    def __upload_attachments(
        self,
        parser: p.XCReportParser,
        summary: p.ActionTestActivitySummary,
        qase: QaseApi,
    ) -> List[str]:
        # Find attachments
        attachments = self.__find_all_attachments(summary)
        if not attachments:
            return []
        attachments_to_upload = []
        for attachment in attachments:
            if attachment.type_identifier not in ATTACHMENT_TYPES:
                continue
            binary_data = parser.open_attachment(attachment.payload_ref.obj_id)
            if binary_data is None:
                continue
            attachments_to_upload.append(
                (
                    binary_data,
                    ATTACHMENT_TYPES[attachment.type_identifier],
                    attachment.name,
                ),
            )

        if not attachments_to_upload:
            return []

        result: List[AttachmentCreated] = qase.attachments.upload(
            self.project_code, *attachments_to_upload
        )
        files = list(map(lambda x: x.hash, result))
        return files

    def __create_comment(
        self, summary: p.ActionTestActivitySummary, prefix: str = ""
    ) -> str:
        if self.__is_system_summary(summary):
            return ""

        if prefix:
            buffer = "{}- {}\n".format(prefix, summary.title)
        else:
            buffer = "{}\n".format(summary.title)

        for sub in summary.subactivities:
            buffer += self.__create_comment(sub, "  {}".format(prefix))
        return buffer

    def __is_system_summary(self, summary: p.ActionTestActivitySummary):
        if summary.activity_type == p.ActivityType.ATTACHMENT_CONTAINER:
            for attachment in summary.attachments:
                if attachment.name in self._ignored_attachment_names:
                    return True
        return False
