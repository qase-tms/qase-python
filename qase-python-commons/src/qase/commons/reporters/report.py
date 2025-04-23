import time
import os
import shutil
import json
import re
from ..models import Result, Run, Attachment
from .. import QaseUtils, Logger
from ..models.config.connection import Format
from ..models.config.qaseconfig import QaseConfig


class QaseReport:
    def __init__(
            self,
            config: QaseConfig,
            logger: Logger
    ):
        self.duration = 0
        self.results = []
        self.attachments = []
        self.config = config
        self.logger = logger

        self.report_path = self.config.report.connection.path
        self.format = self.config.report.connection.format

        self.start_time = None
        self.end_time = None
        self.run_id = None
        self.environment = self.config.environment

    def start_run(self):
        self._check_report_path()
        self.start_time = str(time.time())

    def complete_run(self):
        self.end_time = str(time.time())
        self._compile_report()

    def complete_worker(self):
        pass

    def add_result(self, result: Result):
        for attachment in result.attachments:
            self._persist_attachment(attachment)

        if result.steps:
            self._persist_attachments_in_steps(result.steps)

        self._store_result(result)

    def set_run_id(self, run_id):
        self.run_id = run_id

    def add_attachment(self, attachment: Attachment) -> None:
        self.attachments.append(attachment)

    def get_results(self):
        return self.results

    def set_results(self, results):
        self.results = results

    def _persist_attachment(self, attachment: Attachment):
        if attachment.content:
            if isinstance(attachment.content, str):
                mode = "w"
            if isinstance(attachment.content, bytes):
                mode = "wb"

            file_path = f"{self.report_path}/attachments/{attachment.id}-{attachment.file_name}"
            with open(file_path, mode) as f:
                f.write(attachment.content)
            # Clear content to save memory and avoid double writing
            attachment.content = None
            attachment.file_path = file_path

        elif attachment.file_path:
            file_path = f"{self.report_path}/attachments/{attachment.id}-{attachment.file_name}"
            shutil.copy2(os.path.abspath(attachment.file_path),
                         f"{self.report_path}/attachments/{attachment.id}-{attachment.file_name}")
            attachment.file_path = file_path

    def _persist_attachments_in_steps(self, steps: list):
        for step in steps:
            if step.execution.attachments:
                for attachment in step.execution.attachments:
                    self._persist_attachment(attachment)
                if step.steps:
                    self._persist_attachments_in_steps(step.steps)

    # Method saves result to a file
    def _store_result(self, result: Result):
        self._store_object(result, self.report_path + "/results/", result.id)

    def _check_report_path(self):
        for path in [self.report_path, self.report_path + "/results/", self.report_path + "/attachments/"]:
            self._recreate_dir(path)

    @staticmethod
    def _recreate_dir(path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    def _update_run_duration(self, time):
        self.duration += time

    # Method builds final report
    def _compile_report(self):
        run = Run(
            title="Test run",
            start_time=float(self.start_time),
            end_time=float(self.end_time),
            environment=self.environment
        )
        for file in os.listdir(self.report_path + "/results"):
            with open(self.report_path + "/results/" + file, 'r') as source:
                result = self._read_object(source)
                run.add_result(result)

        run.add_host_data(QaseUtils.get_host_data())

        self._store_object(run, self.report_path, "report")

    # Saves a model to a file
    def _store_object(self, object, path, filename):
        data = object.__str__()
        if self.format == Format.jsonp:
            data = f"qaseJsonp({data});"
        with open(f"{path}/{filename}.{self.format.value}", 'w', encoding='utf-8') as f:
            f.write(data)

    def _read_object(self, source):
        data = source.read()
        if self.format == Format.json:
            return json.loads(data)
        elif self.format == Format.jsonp:
            jsonp_pattern = r'\w+\(\s*({[\s\S]*})\s*\);'
            match = re.search(jsonp_pattern, data)
            if match:
                data = match.group(1)
                return json.loads(data)
            else:
                raise ValueError('Invalid JSONP format')
        raise ValueError('Unknown format')
