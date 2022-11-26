import json
from pathlib import Path

class Report:
    def __init__(
        self, 
        report_path = "build/qase-report"
    ):
        self.report_path = report_path

        self.results = []
        self.attachments = {}

        self._check_report_path()

        pass

    def add_result(self, result, steps):
        file = self.report_path + '/' + result.get('uuid') + '.json'
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        pass

    def start_run(self, hash):
        print()
        print(
            "Starting Qase Report"
        )
        pass

    def complete_run(self, is_main=True, exit_code = None):
        pass

    def _check_report_path(self):
        Path(self.report_path).mkdir(parents=True, exist_ok=True)
