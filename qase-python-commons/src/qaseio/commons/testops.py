from qaseio.api_client import ApiClient
from qaseio.configuration import Configuration
from qaseio.api.attachments_api import AttachmentsApi
from qaseio.api.environments_api import EnvironmentsApi
from qaseio.api.projects_api import ProjectsApi
from qaseio.api.results_api import ResultsApi
from qaseio.api.runs_api import RunsApi
from qaseio.model.run_create import RunCreate
from qaseio.model.result_create_bulk import ResultCreateBulk
from qaseio.model.result_create import ResultCreate
from qaseio.model.result_create_case import ResultCreateCase
from qaseio.rest import ApiException
from qaseio.commons.models.attachment import Attachment
from qaseio.commons.models.step import Step

from qaseio.commons.models.result import Result

from datetime import datetime
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

class QaseTestOps:

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
        configuration.host = f'https://api.{host}/v1'
        configuration.ssl_ca_cert = certifi.where()

        self.client = ApiClient(configuration)

        parseBool = lambda d : d in ("y", "yes", "true", "1", 1, True)

        self.project_code = project_code
        self.run_id = int(run_id) if run_id else run_id
        self.plan_id = int(plan_id) if plan_id else plan_id
        self.bulk = parseBool(bulk)
        self.defect = parseBool(defect)
        self.complete_after_run = parseBool(complete_run)
        self.environment = None
        self.host = host
        self.enabled = True
        self.chunk_size = min(2000, max(10, int(chunk_size)))
        if environment:
            if isinstance(environment, int) or (isinstance(environment, str) and environment.isnumeric()):
                self.environment = environment
            elif isinstance(environment, str):
                self.environment = self._get_environment(environment, self.project_code)

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
                print("[Qase] ⚠️  Disabling Qase TestOps reporter. Exception when calling ProjectApi->get_project: %s\n" % e)

    # Method loads environment by name and returns environment id
    def _get_environment(self, environment: str, project: str):
        if self.enabled:
            api_instance = EnvironmentsApi(self.client)
            response = api_instance.get_environments(code=project)
            if hasattr(response, 'result'):
                for env in response["result"]["entities"]:
                    if env["slug"] == environment:
                        return env["id"]
        return None

    def _send_bulk_results(self):
        if self.enabled and self.results:
            print()
            print(f"[Qase] Uploading attachments for Run ID: {self.run_id}...")
            results = []
            for result in self.results:
                attached = []
                if result.attachments:
                    for attachment in result.attachments:
                        attached.extend(self._upload(attachment))

                steps = []
                for step in result.steps:
                    prepared = self._prepare_step(step)
                    steps.append(prepared)

                case_data = {
                    "title": result.get_title(),
                    "description": result.get_field('description'),
                    "precondtions": result.get_field('precondtions'),
                    "postconditions": result.get_field('postconditions'),
                }

                for key, param in result.params.items():
                    # Hack to match old TestOps API
                    if param == "": result.params[key] = "empty"

                if (result.get_field('severity')):
                    case_data["severity"] = result.get_field('severity')

                if (result.get_field('priority')):
                    case_data["priority"] = result.get_field('priority')

                if (result.get_field('layer')):
                    case_data["layer"] = result.get_field('layer')

                if result.get_suite_title():
                    case_data["suite_title"] = "\t".join(result.get_suite_title().split("."))

                results.append({
                    "case_id": result.get_testops_id(),
                    "status": result.execution.status,
                    "stacktrace": result.execution.stacktrace,
                    "time_ms": result.execution.duration,
                    "comment": result.message,
                    "attachments": [attach.hash for attach in attached],
                    "case": case_data,
                    "steps": steps,
                    "param": result.params,
                    "defect": self.defect
                })

            api_results = ResultsApi(self.client)
            print(f"[Qase] Sending results to test run {self.run_id}. Total results: {len(results)}. Results in a chunk: {self.chunk_size}.")

            i = 1

            for chunk in more_itertools.chunked(results, self.chunk_size):
                try:
                    print(f"[Qase] Sending chunk #{i}. Chunk size: {len(chunk)}... ")
                    api_results.create_result_bulk(
                        code=self.project_code,
                        id=self.run_id,
                        result_create_bulk=ResultCreateBulk(
                            results=chunk
                        )
                    )
                    print(f"[Qase] Chunk #{i} was sent successfully.")
                    i = i+1
                except Exception as e:
                    print(f"[Qase] ⚠️  Error at sending results for run {self.run_id} (Chunk #{i}): {e}")
                    raise e

    def _complete_run(self):
        if self.enabled:
            api_runs = RunsApi(self.client)
            print(f"[Qase] Completing run {self.run_id}")
            res = api_runs.get_run(self.project_code, self.run_id).result
            if res.status == 1:
                print(f"[Qase] Run ID:{self.run_id} already finished")
                return
            try:
                api_runs.complete_run(self.project_code, self.run_id)
                print(f"[Qase] Run ID:{self.run_id} was completed successfully")
            except Exception as e:
                print(f"[Qase] ⚠️  Run ID:{self.run_id} was completed with error: {e}")

    def _check_run(self):
        if self.enabled:
            if self.plan_id and not self.run_id:
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
                    "[Qase] TestOps: created test run "
                    "https://app.{}/run/{}/dashboard/{}".format(
                        self.host, self.project_code, self.run_id
                    )
                )
            except Exception as e:
                self.enabled = False
                print()
                print(f"[Qase] ⚠️  Disabling Qase TestOps reporter. Unable to create test run: {e}")

    def _upload(self, attachment: Attachment):
        api_attachments = AttachmentsApi(self.client)

        return api_attachments.upload_attachment(
                self.project_code, file=[attachment.get_for_upload()],
            ).result
    
    # This method contains a lot of hacks to match old TestOps API.
    def _prepare_step(self, step: Step):
        prepared_children = []

        prepared_step = {
            "time": step.execution.duration,
        }
        
        prepared_step["status"] = step.execution.status
        if step.execution.status == 'untested':
            prepared_step["status"] = 'passed'
        
        if step.step_type == "text":
            prepared_step['action'] = step.data.action
            if step.data.expected_result:
                prepared_step['expected_result'] = step.data.expected_result
        
        if step.step_type == "request":
            prepared_step['action'] = step.data.request_method + " " + step.data.request_url
            if (step.data.request_body):
                step.attachments.append(Attachment(file_name='request_body.txt', content=step.data.request_body, mime_type='text/plain'))
            if (step.data.request_headers):
                step.attachments.append(Attachment(file_name='request_headers.txt', content=step.data.request_headers, mime_type='text/plain'))
            if (step.data.response_body):
                step.attachments.append(Attachment(file_name='response_body.txt', content=step.data.response_body, mime_type='text/plain'))
            if (step.data.response_headers):
                step.attachments.append(Attachment(file_name='response_headers.txt', content=step.data.response_headers, mime_type='text/plain'))

        if step.attachments:
            uploaded_attachments = []
            for file in step.attachments:
                uploaded_attachments.extend(self._upload(file))
            prepared_step['attachments'] = [attach.hash for attach in uploaded_attachments]

        if step.steps:
            for substep in step.steps:
                prepared_children.append(self._prepare_step(substep))
            prepared_step["steps"] = prepared_children
        return prepared_step

    def _send_result(self, result: Result):
        if self.enabled:
            api_results = ResultsApi(self.client)
            print()
            print(f"[Qase] Sending a result to test run {self.run_id}...")

            attached = []
            if result.attachments:
                for attachment in result.attachments:
                    attached.extend(self._upload(attachment))

            steps = []
            for step in result.steps:
                prepared = self._prepare_step(step)
                steps.append(prepared)

            case_data = {
                "title": result.get_title(),
                "description": result.get_field('description'),
                "precondtions": result.get_field('precondtions'),
                "postconditions": result.get_field('postconditions'),
            }

            for key, param in result.params.items():
                # Hack to match old TestOps API
                if param == "":
                    result.params[key] = "empty"

            if (result.get_field('severity')):
                case_data["severity"] = result.get_field('severity')

            if (result.get_field('priority')):
                case_data["priority"] = result.get_field('priority')

            if (result.get_field('layer')):
                case_data["layer"] = result.get_field('layer')

            if result.get_suite_title():
                case_data["suite_title"] = "\t".join(result.get_suite_title().split("."))

            try:
                api_results.create_result(
                    code=self.project_code,
                    id=self.run_id,
                    result_create=ResultCreate(
                        case_id=result.get_testops_id(),
                        status=result.execution.status,
                        stacktrace=result.execution.stacktrace,
                        time_ms=result.execution.duration,
                        comment=result.message,
                        attachments = [attach.hash for attach in attached],
                        defect=self.defect,
                        case=ResultCreateCase(
                            **{k: v for k, v in case_data.items() if v is not None}
                        ),
                        steps=steps,
                        param=result.params
                    )
                )
                print(f"[Qase] Results of run {self.run_id} was sent")
            except Exception as e:
                print(f"[Qase] ⚠️  Error at sending results for run {self.run_id}: {e}")
                raise e

    # Lifecycle methods
    def start_run(self):
        if self.enabled:
            """Verify test run"""
            self._check_run()
            return self.run_id

    def complete_run(self, is_main=True, exit_code=None):
        if self.enabled:
            if self.bulk:
                self._send_bulk_results()
            if self.complete_after_run and is_main:
                self._complete_run()

    def add_result(self, result: Result):
        if self.enabled:
            if self.bulk:
                self.results.append(result)
            else:
                self._send_result(result)
