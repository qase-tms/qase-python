from qaseio.api_client import ApiClient
from qaseio.configuration import Configuration
from qaseio.api.attachments_api import AttachmentsApi
from qaseio.api.plans_api import PlansApi
from qaseio.api.projects_api import ProjectsApi
from qaseio.api.results_api import ResultsApi
from qaseio.api.runs_api import RunsApi
from qaseio.model.run_create import RunCreate
from qaseio.model.result_create_bulk import ResultCreateBulk
from qaseio.model.result_create import ResultCreate
from qaseio.model.result_create_case import ResultCreateCase
from qaseio.rest import ApiException

from datetime import datetime
from typing import Tuple, Union
import mimetypes
import ntpath
import certifi

from io import BytesIO

from pkg_resources import DistributionNotFound, get_distribution

def package_version(name):
    try:
        version = get_distribution(name).version
    except DistributionNotFound:
        version = "unknown"
    return version

class TestOpsRunNotFoundException(Exception):
    pass

class QaseTestOps:

    def __init__(self,
            api_token,
            project_code,
            run_id=None,
            plan_id=None,
            mode="async",
            run_title=None,
            environment=None,
            host="qase.io",
            complete_run=False) -> None:

        configuration = Configuration()
        configuration.api_key['TokenAuth'] = api_token
        configuration.host = f'https://api.{host}/v1'
        configuration.ssl_ca_cert = certifi.where()

        self.client = ApiClient(configuration)

        self.project_code = project_code
        self.run_id = int(run_id) if run_id else run_id
        self.plan_id = plan_id
        self.mode = mode
        self.complete_after_run = complete_run
        self.environment = int(environment) if environment else environment
        self.host = host
        self.enabled = True

        if run_title and run_title != '':
            self.run_title = run_title
        else:
            self.run_title = "Automated Run {}".format(str(datetime.now()))

        self.run = None

        self.results = []
        self.attachments = {}

        """Verify that project exists in TestOps"""
        self._get_project(self.project_code)

    def _get_project(self, project):
        if self.enabled:
            api_instance = ProjectsApi(self.client)
            try:
                response = api_instance.get_project(code=project)
                if hasattr(response, 'result'):
                    return response.result
                raise ValueError("Unable to find given project code")
            except ApiException as e:
                self.enabled = False
                print("Disabling Qase TestOps reporter. Exception when calling ProjectApi->get_project: %s\n" % e)

    def _send_bulk_results(self):
        if self.enabled and self.results:
            print()
            print(f"Uploading attachments for Run ID: {self.run_id}...")
            results = []
            for result in self.results:
                attached = []
                for files in result.get('attachments', []):
                    attached.extend(self._upload(self.project_code, files))
                    result['attachments'] = [attach.hash for attach in attached]

                steps = []
                for step in result['steps']:
                    prepared = self._prepare_step(step)
                    steps.append(prepared)

                result['steps'] = steps

                results.append(result)

            api_results = ResultsApi(self.client)
            print()
            print(f"Sending results to test run {self.run_id}...")
            try:
                api_results.create_result_bulk(
                    code=self.project_code,
                    id=self.run_id,
                    result_create_bulk=ResultCreateBulk(
                        results=results
                    )
                )
                print(f"Results of run {self.run_id} are sent")
            except Exception as e:
                print(f"Error at sending results for run {self.run_id}: {e}")

    def _complete_run(self):
        if self.enabled:
            api_runs = RunsApi(self.client)
            print()
            print(f"Completing run {self.run_id}")
            res = api_runs.get_run(self.project_code, self.run_id).result
            if res.status == 1:
                print(f"Run ID:{self.run_id} already finished")
                return
            try:
                api_runs.complete_run(self.project_code, self.run_id)
                print(f"Run ID:{self.run_id} was finished successfully")
            except Exception as e:
                print(f"Run ID:{self.run_id} was finished with error: {e}")

    def _check_run(self):
        if self.enabled:
            if self.run_id and self.plan_id:
                raise ValueError(
                    "You should provide either use test run or test plan"
                )
            if self.plan_id:
                api_plans = PlansApi(self.client)
                plan = api_plans.get_plan(
                    code=self.project_code,
                    id=int(self.plan_id)
                )
                if not plan:
                    raise ValueError("Could not find test plan")
                self._create_run(plan_id=self.plan_id, environment_id=self.environment)
            if not self.run_id and not self.plan_id:
                self._create_run(environment_id=self.environment)
                pass
            if not self.run and not self._load_run:
                raise TestOpsRunNotFoundException(
                    "Unable to find given test run."
                )

    def set_run_id(self, run_id):
        self.run_id = int(run_id)

    def _load_run(self):
        if self.enabled:
            api_runs = RunsApi(self.client)
            if self.run_id:
                run = api_runs.get_run(
                    code=self.project_code,
                    id=self.run_id,
                ).result
                if run.id:
                    return True
                return False

    def _create_run(self, plan_id=None, environment_id=None, cases=[]):
        if self.enabled:
            api_runs = RunsApi(self.client)
            kwargs = dict(
                    title=self.run_title,
                    cases=cases,
                    environment_id=(int(environment_id) if environment_id else None),
                    plan_id=(int(plan_id) if plan_id else plan_id),
                    is_autotest=True
            )
            try:
                result = api_runs.create_run(
                    code=self.project_code,
                    run_create=RunCreate(**{k: v for k, v in kwargs.items() if v is not None})
                )
                self.run_id = result.result.id
                self.run = result.result

                print()
                print(
                    "Qase TestOps: created test run "
                    "https://app.{}/run/{}/dashboard/{}".format(
                        self.host, self.project_code, self.run_id
                    )
                )
            except Exception as e:
                self.enabled = False
                print()
                print(f"Disabling Qase TestOps reporter. Unable to create test run: {e}")

    def _upload(
        self,
        code: str,
        *file_infos: Union[str, Tuple[str, str], Tuple[bytes, str, str]],
    ):
        api_attachments = AttachmentsApi(self.client)
        for _id, file in enumerate(file_infos):
            filename = None
            if isinstance(file, tuple):
                if len(file) == 2:
                    path, mime = file
                else:
                    path, mime, filename = file
            else:
                path = file
                mime = mimetypes.guess_type(file)[0]
            if isinstance(path, bytes):
                content = BytesIO(path)
                content.name = filename or ntpath.basename(path)
                content.mime = mime
            else:
                content = open(path, "rb")

            return api_attachments.upload_attachment(
                self.project_code, file=[content],
            ).result

    def _prepare_step(self, step):
        if step['attachments']:
            attached_step = []
            for files in step['attachments']:
                attached_step.extend(self._upload(self.project_code, files))
            step["attachments"] = [attach.hash for attach in attached_step]
        if step['steps']:
            prepared = []
            for substep in step['steps']:
                prepared.append(self._prepare_step(substep))
            step['steps'] = prepared
        return step

    def _send_result(self, result):
        if self.enabled:
            api_results = ResultsApi(self.client)
            print()
            print(f"Sending a result to test run {self.run_id}...")

            attachments = result.get("attachments", [])
            attached = []
            if attachments:
                for files in attachments:
                    attached.extend(self._upload(self.project_code, files))

            steps = []
            for step in result['steps']:
                prepared = self._prepare_step(step)
                steps.append(prepared)

            case_data = {
                "title": result.get('case').get('title'),
                "description": result.get('case').get('description', ''),
                "precondtions": result.get('case').get('precondtions', ''),
                "postconditions": result.get('case').get('postconditions', ''),
            }

            if (result.get('case').get('severity', None)):
                case_data["severity"] = result.get('case').get('severity')

            if (result.get('case').get('layer', None)):
                case_data["layer"] = result.get('case').get('layer')

            try:
                api_results.create_result(
                    code=self.project_code,
                    id=self.run_id,
                    result_create=ResultCreate(
                        case_id=result.get('case_id', 0),
                        status=result.get('status'),
                        stacktrace=result.get('stacktrace'),
                        time_ms=result.get('time_ms'),
                        comment=result.get('comment', ''),
                        attachments = [attach.hash for attach in attached],
                        case=ResultCreateCase(
                            **{k: v for k, v in case_data.items() if v is not None}
                        ),
                        steps=steps,
                        param=result.get('param', {})
                    )
                )
                print(f"Results of run {self.run_id} was sent")
            except Exception as e:
                print(f"Error dat sending results for run {self.run_id}: {e}")
            pass

    # Lifecycle methods
    def start_run(self):
        if self.enabled:
            """Verify test run"""
            self._check_run()
            return self.run_id

    def complete_run(self, is_main=True, exit_code=None):
        if self.enabled:
            if self.mode == "async":
                self._send_bulk_results()
            if self.complete_after_run and is_main:
                self._complete_run()

    def add_result(self, result, steps):
        if self.enabled:
            result['steps'] = self._get_steps(steps)
            if self.mode == "sync":
                self._send_result(result)
                pass
            else:
                self.results.append(result)
                pass

    def _get_steps(self, steps):
        tree = []
        for uuid in steps:
            branch = []
            if steps[uuid].get('steps', []):
                branch = self._get_steps(steps[uuid].get('steps', {}))
            steps[uuid]['steps'] = branch
            tree.append({**steps[uuid]})
        return tree