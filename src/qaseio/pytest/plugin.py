from qaseio.client import QaseApi


class QasePytestPlugin:
    def __init__(self, api_token, project, testrun=None):
        self.client = QaseApi(api_token)
        self.project_code = project
        self.testrun_id = testrun

    def pytest_report_header(self, config, startdir):
        """ Add extra-info in header """
        message = "pytest-qase: "
        if self.testrun_id:
            message += "existing testrun #{} selected".format(self.testrun_id)
        else:
            message += "a new testrun will be created"
        return message
