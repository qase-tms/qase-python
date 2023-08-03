import json

from qaseio.api_client import ApiClient
from qaseio.api.result_api import ResultApi
from qaseio.configuration import Configuration
from qaseio.model.create_results_request_v2 import CreateResultsRequestV2
from qaseio.model.create_results_request_v2_results_inner import CreateResultsRequestV2ResultsInner
from qaseio.model.result_execution import ResultExecution
from qaseio.model.result_attachment import ResultAttachment
from qaseio.model.result_step import ResultStep
from qaseio.model.result_relations import ResultRelations
from qaseio.commons.testops import QaseTestOps

import more_itertools
import certifi

from pkg_resources import DistributionNotFound, get_distribution


def package_version(name):
    try:
        version = get_distribution(name).version
    except DistributionNotFound:
        version = "unknown"
    return version


class TestOpsRunNotFoundException(Exception):
    pass


class QaseTestOpsV2(QaseTestOps):

    def __init__(self,
                 api_token,
                 project_code,
                 run_id=None,
                 plan_id=None,
                 bulk=True,
                 run_title=None,
                 environment=None,
                 host="qase.io",
                 complete_run=False,
                 defect=False,
                 chunk_size=200) -> None:

        configuration = Configuration()
        configuration.api_key['TokenAuth'] = api_token
        configuration.host = f'https://api.{host}'
        configuration.ssl_ca_cert = certifi.where()

        self.clientv2 = ApiClient(configuration)

        super().__init__(
            api_token=api_token,
            project_code=project_code,
            run_id=run_id,
            plan_id=plan_id,
            bulk=bulk,
            run_title=run_title,
            environment=environment,
            host=host,
            complete_run=complete_run,
            defect=defect,
            chunk_size=chunk_size
        )

    def _send_bulk_results(self):
        def filter_dict(dct):
            return {k: v for k, v in dct.items() if v}

        def to_dict(obj):
            return json.loads(
                json.dumps(obj, default=lambda o: filter_dict(getattr(o, '__dict__', str(o))))
            )

        if self.enabled and self.results:
            print(f"[Qase] Uploading attachments for Run ID: {self.run_id}...")
            results = []
            for result in self.results:
                d = to_dict(result)

                if 'execution' in d:
                    d['execution'] = ResultExecution(d['execution'])
                if 'attachment' in d:
                    d['attachment'] = ResultAttachment(d['attachment'])
                if 'step' in d:
                    d['step'] = ResultStep(d['step'])
                if 'relations' in d:
                    d['relations'] = ResultRelations(d['relations'])

                results.append(CreateResultsRequestV2ResultsInner(d))

            api_results = ResultApi(self.clientv2)
            print(f"[Qase] Sending results to test run {self.run_id}. Total results: {len(results)}. Results in a "
                  f"chunk: {self.chunk_size}.")

            i = 1

            for chunk in more_itertools.chunked(results, self.chunk_size):
                try:
                    print(f"[Qase] Sending chunk #{i}. Chunk size: {len(chunk)}... ")
                    api_results.create_results_v2(
                        self.project_code,
                        self.run_id,
                        CreateResultsRequestV2(
                            results=chunk
                        )
                    )
                    print(f"[Qase] Chunk #{i} was sent successfully.")
                    i = i+1
                except Exception as e:
                    print(f"[Qase] ⚠️  Error at sending results for run {self.run_id} (Chunk #{i}): {e}")
                    raise e
