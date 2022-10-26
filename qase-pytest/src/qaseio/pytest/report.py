class Report:
    def __init__(
        self, 
        report_path = "build/qase-report"
    ):
        self.report_path = report_path

        self.results = []
        self.attachments = {}

        pass

    def add_result(self, result):
        pass

    def start_run(self, hash):
        pass

    def complete_run(self, exit_code = None):
        pass