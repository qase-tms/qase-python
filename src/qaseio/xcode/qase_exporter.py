import json
from typing import Optional, Dict, List

import attr
from qaseio.client import QaseApi
from qaseio.client.models import TestRunCreate, TestRunResultCreate, TestRunResultStatus, \
    TestRunResultStepCreate, MimeTypes, AttachmentCreated
from qaseio.client.services import BadRequestException
from qaseio.xcreport.parser import *

ACTION_TEST_SUMMARY_TO_QASE_STATUS = {
    TestStatus.FAULURE: TestRunResultStatus.FAILED,
    TestStatus.UNDEFINE: TestRunResultStatus.FAILED,
    TestStatus.SUCCESS: TestRunResultStatus.PASSED
}

ATTACHMENT_TYPES = {
    UniformTypeIdentifier.PNG: MimeTypes.PNG
}


QASE_STEP_MARKER_FILE = "Qase step marker"
QASE_CONFIG_FILE = "Qase config"


@attr.s
class QaseExtractor:
    xc_path: str = attr.ib()
    api_token: str = attr.ib()
    project_code: str = attr.ib()
    upload_attachments: bool = attr.ib(default=True)
    test_run_name: str = attr.ib(default="Run")

    def __attrs_post_init__(self):
        self._parser = XCReportParser(self.xc_path)
        self._ignored_attachment_names = [QASE_STEP_MARKER_FILE, QASE_CONFIG_FILE]

    def process(self):
        report = self._parser.open_report_object()
        tests = self._parser.extract_tests(report)
        tests_with_qase: Dict[int: ActionTestSummary] = {}
        qase_ids: List[int] = []
        for test in tests:
            case_id = self.__find_case_id(test)
            if case_id is None:
                continue
            qase_ids.append(int(case_id))
            tests_with_qase[case_id] = test

        qase = QaseApi(self.api_token)

        test_run = qase.runs.create(
            self.project_code,
            TestRunCreate(self.test_run_name, qase_ids)
        )

        for case_id, test in tests_with_qase.items():
            steps: List[TestRunResultStepCreate] = []
            # Find steps
            position = 1
            for activity_summary in test.activity_summaries:
                if not self.__contains_step_mark(activity_summary):
                    continue
                files = self.__upload_attachments(activity_summary, qase) if self.upload_attachments else []
                # Prepare step
                contains_failure = self.__activity_summary_contains_type(activity_summary, ActivityType.FAILURE)
                steps.append(
                    TestRunResultStepCreate(
                        position,
                        TestRunResultStatus.FAILED if contains_failure else TestRunResultStatus.PASSED,
                        files
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
                        steps=steps
                    )
                )
            except BadRequestException:
                # Try without steps
                qase.results.create(
                    self.project_code,
                    test_run.id,
                    TestRunResultCreate(
                        case_id,
                        ACTION_TEST_SUMMARY_TO_QASE_STATUS[test.test_status],
                        int(test.duration),
                        comment="Check number of steps in your code. They are not equaly."
                    )
                )

    def __extract_qase_config(self, test_summary: ActionTestSummary):
        for activity_summary in test_summary.activity_summaries:
            binary_data = self._parser.extract_attachment_from_activity_summary(activity_summary, QASE_CONFIG_FILE)
            if binary_data is not None:
                config = json.loads(binary_data)
                return config

    def __activity_is_step_mark(self, activity_summary: ActionTestActivitySummary):
        mark = self._parser.extract_attachment_from_activity_summary(activity_summary, QASE_STEP_MARKER_FILE)
        return mark is not None

    def __contains_step_mark(self, activity_summary: ActionTestActivitySummary):
        for sub_activity_summary in activity_summary.subactivities:
            if self.__activity_is_step_mark(sub_activity_summary):
                return True
        return False

    def __activity_summary_contains_type(self, activity_summary: ActionTestActivitySummary, act_type: ActivityType):
        if activity_summary.activity_type == act_type:
            return True
        else:
            for subactivity in activity_summary.subactivities:
                return self.__activity_summary_contains_type(subactivity, act_type)

        return False

    def __find_all_attachments(self, summary: ActionTestActivitySummary) -> List[ActionTestAttachment]:
        result: List[ActionTestAttachment] = []
        if summary.activity_type == ActivityType.ATTACHMENT_CONTAINER:
            filtered = list(filter(
                lambda a: a.name not in self._ignored_attachment_names and a.payload_ref is not None,
                summary.attachments
            ))
            result.extend(filtered)
        for sub in summary.subactivities:
            subResult = self.__find_all_attachments(sub)
            result.extend(subResult)
        return result

    def __find_case_id(self, test_summary: ActionTestSummary) -> Optional[str]:
        test_config = self.__extract_qase_config(test_summary)
        if test_config is None:
            return None
        return test_config["caseId"]

    def __upload_attachments(self, summary: ActionTestActivitySummary, qase: QaseApi) -> List[str]:
        # Find attachments
        attachments = self.__find_all_attachments(summary)
        if not attachments:
            return []
        attachments_to_upload = []
        for attachment in attachments:
            if attachment.type_identifier not in ATTACHMENT_TYPES:
                continue
            binary_data = self._parser.open_attachment(attachment.payload_ref.obj_id)
            if binary_data is None:
                continue
            attachments_to_upload.append(
                (binary_data, ATTACHMENT_TYPES[attachment.type_identifier], attachment.name),
            )

        result: List[AttachmentCreated] = qase.attachments.upload(
            self.project_code,
            *attachments_to_upload
        )
        files = list(map(lambda x: x.hash, result))
        return files
