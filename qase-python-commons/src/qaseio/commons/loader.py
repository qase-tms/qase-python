from qaseio.api_client import ApiClient
from qaseio.configuration import Configuration
from qaseio.api.plans_api import PlansApi
from qaseio.api.runs_api import RunsApi
from qaseio.rest import ApiException
import certifi

class TestOpsPlanLoader:
    def __init__(self, api_token, host = 'qase.io'):
        configuration = Configuration()
        configuration.api_key['TokenAuth'] = api_token
        configuration.host = f'https://api.{host}/v1'

        self.client = ApiClient(configuration)
        self.case_list = []

        configuration.ssl_ca_cert = certifi.where()

    def load(
            self, code: str, plan_id: int, run_id: str | None, rerun: bool
    ) -> list:
        # if run_id is specified check first if there are tests, if they are, ignore plan_id and use cases from there
        # if run_id is empty, get all cases from plan_id (Jenkins plugin)

        if type(rerun) is not bool:
            rerun = True if rerun in ['true', 'True', '1', 1] else False

        if rerun and run_id is None:
            raise EnvironmentError("RUN ID needs to be specified for rerun")
        test_run_cases = []
        if run_id:
            test_run_cases = self._get_cases_form_test_run(
                code, int(run_id), rerun
            )
        # use test run_if first
        if test_run_cases:
            self.case_list = test_run_cases
        # if run was empty or fully completed in case of rerun use cases from the test plan_id
        elif rerun is False:
            self.case_list = self._get_cases_from_test_plan(code, plan_id)
        # nothing to do
        else:
            self.case_list = []
        print(f"[Qase] ⚠️  {code} test case list to start: {self.case_list}")
        return self.case_list

    def _get_cases_from_test_plan(self, code: str, plan_id: int):
        print(f"[Qase] ⚠️  Getting {code} tests cases from test plan: {plan_id}")
        api_instance = PlansApi(self.client)
        try:
            response = api_instance.get_plan(code=code, id=plan_id)
            if hasattr(response, "result"):
                return [c.case_id for c in response.result.cases]
            raise ValueError("Unable to find given plan")
        except ApiException as e:
            print("Unable to load test plan data: %s\n" % e)
        return []

    def _get_cases_form_test_run(self, code: str, run_id: int, rerun: bool):
        print(f"[Qase] ⚠️  Getting {code} tests cases from run: {run_id}, {rerun=}")
        run_api_instance = RunsApi(self.client)
        try:
            response = run_api_instance.get_run(code, run_id, include="cases")
            if hasattr(response, "result"):
                return response.result.cases
                # TODO: check test case status, API provides only list of cases
        except ApiException as e:
            print("Unable to load test run data: %s\n" % e)
        return []
