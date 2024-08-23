from qase.api_client_v1.api_client import ApiClient
from qase.api_client_v1.configuration import Configuration
from qase.api_client_v1.api.plans_api import PlansApi
from qase.api_client_v1.exceptions import ApiException

import certifi


class TestOpsPlanLoader:
    def __init__(self, api_token, host='qase.io'):
        configuration = Configuration()
        configuration.api_key['TokenAuth'] = api_token
        configuration.host = f'https://api.{host}/v1'
        configuration.ssl_ca_cert = certifi.where()

        self.client = ApiClient(configuration)
        self.case_list = []

    def load(self, code: str, plan_id: int) -> list:
        try:
            response = PlansApi(self.client).get_plan(code=code, id=plan_id)
            if hasattr(response, 'result'):
                self.case_list = [c.case_id for c in response.result.cases]
                return self.case_list
            raise ValueError("Unable to find given plan")
        except ApiException as e:
            print("Unable to load test plan data: %s\n" % e)
        return []
