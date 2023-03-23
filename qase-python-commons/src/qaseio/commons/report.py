from pathlib import Path
class QaseReport:
    def __init__(
        self, 
        report_path = "build/qase-report",
        format = "json"
    ):
        self.report_path = report_path
        self.format = format

        self.results = []
        self.attachments = {}

        self._check_report_path()

        pass

    def add_result(self, result, steps):
        # TBD
        pass

    def start_run(self):
        # TBD
        pass

    def complete_run(self, is_main=True, exit_code = None):
        # TBD
        pass

    def _check_report_path(self):
        Path(self.report_path).mkdir(parents=True, exist_ok=True)
