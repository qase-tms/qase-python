import threading
import urllib.parse
import copy

from datetime import datetime
from typing import List, Union, Dict, Optional
from .. import Logger, ReporterException
from ..client.base_api_client import BaseApiClient
from ..models import Result
from ..models.config.qaseconfig import QaseConfig

DEFAULT_BATCH_SIZE = 200
DEFAULT_THREAD_COUNT = 4


class QaseTestOpsMulti:

    def __init__(self, config: QaseConfig, logger: Logger, client: BaseApiClient) -> None:
        self.config = config
        self.logger = logger
        self.__baseUrl = self.__get_host(config.testops.api.host)
        self.client = client

        self.multi_config = config.testops_multi
        self.batch_size = min(2000, max(1, int(self.config.testops.batch.size or DEFAULT_BATCH_SIZE)))
        self.send_semaphore = threading.Semaphore(DEFAULT_THREAD_COUNT)
        self.lock = threading.Lock()
        self.count_running_threads = 0

        # Create dictionary mapping project codes to their configurations
        self.project_configs: Dict[str, Dict] = {}
        for project in self.multi_config.projects:
            self.project_configs[project.code] = {
                'config': project,
                'run_id': None,
                'plan_id': int(project.plan.id) if project.plan and project.plan.id else None,
                'environment': None,
                'run_title': None,
                'run_description': None,
                'complete_after_run': project.run.complete if project.run else True,
            }

        # Initialize structures for grouping results by projects
        self.project_results: Dict[str, List[Result]] = {project.code: [] for project in self.multi_config.projects}
        self.project_runs: Dict[str, int] = {}  # Store run_id as int
        self.processed: Dict[str, List[Result]] = {project.code: [] for project in self.multi_config.projects}

        # Initialize environment for each project
        for project_code, project_data in self.project_configs.items():
            project_config = project_data['config']
            environment = project_config.environment or self.config.environment
            
            if environment:
                if isinstance(environment, int) or (isinstance(environment, str) and environment.isnumeric()):
                    project_data['environment'] = environment
                elif isinstance(environment, str):
                    project_data['environment'] = self.client.get_environment(environment, project_code)

            # Set run title and description for each project
            run_title = project_config.run.title if project_config.run else None
            if run_title and run_title != '':
                project_data['run_title'] = run_title
            else:
                project_data['run_title'] = f"Automated Run {project_code} {str(datetime.now())}"

            run_description = project_config.run.description if project_config.run else None
            if run_description and run_description != '':
                project_data['run_description'] = run_description
            else:
                project_data['run_description'] = f"Automated Run {project_code} {str(datetime.now())}"

            # Set run_id if specified in config
            if project_config.run and project_config.run.id:
                project_data['run_id'] = int(project_config.run.id)

        # Verify that all projects exist in TestOps
        for project_code in self.project_configs.keys():
            self.client.get_project(project_code)

    def _create_project_result(self, result: Result, project_code: str, testops_ids: Optional[List[int]]) -> Result:
        """
        Create a copy of result with specific testops_ids for a project.
        
        :param result: Original result
        :param project_code: Project code
        :param testops_ids: List of test case IDs for this project (can be empty or None)
        :return: Copy of result with testops_ids set
        """
        # Create a deep copy of the result
        project_result = copy.deepcopy(result)
        
        # Set testops_ids for this project (can be None or empty list for tests without IDs)
        project_result.testops_ids = testops_ids if testops_ids else None
        
        # Clear project mapping as we're sending to specific project
        project_result.testops_project_mapping = None
        
        return project_result

    def _send_results_threaded(self, project_code: str, run_id: Union[str, int], results: List[Result]):
        try:
            # Convert run_id to str for send_results (it will convert to int internally for API)
            run_id_str = str(run_id) if isinstance(run_id, int) else run_id
            self.client.send_results(project_code, run_id_str, results)
            with self.lock:
                self.processed[project_code].extend(results)
        except Exception as e:
            with self.lock:
                self.logger.log(f"Error at sending results for project {project_code}, run {run_id}: {e}", "error")
            raise
        finally:
            self.count_running_threads -= 1
            self.send_semaphore.release()

    def _send_results_for_project(self, project_code: str) -> None:
        """Send results for a specific project."""
        results = self.project_results[project_code]
        if not results:
            return

        run_id = self.project_runs.get(project_code)
        if not run_id:
            self.logger.log(f"No run_id for project {project_code}, skipping send", "warning")
            return

        # Filter results by status if status_filter is configured
        results_to_send = results.copy()
        
        if self.config.testops.status_filter and len(self.config.testops.status_filter) > 0:
            filtered_results = []
            for result in results_to_send:
                result_status = result.get_status()
                if result_status and result_status not in self.config.testops.status_filter:
                    filtered_results.append(result)
                else:
                    self.logger.log_debug(f"Filtering out result '{result.title}' with status '{result_status}' for project {project_code}")
            
            results_to_send = filtered_results
            self.logger.log_debug(f"Filtered {len(results) - len(results_to_send)} results by status filter for project {project_code}")
        
        if results_to_send:
            # Acquire semaphore before starting the send operation
            self.send_semaphore.acquire()
            self.count_running_threads += 1

            # Start a new thread for sending results
            # run_id is stored as int, convert to str for thread (will be converted back to int in send_results)
            run_id_for_thread = str(run_id) if isinstance(run_id, int) else run_id
            send_thread = threading.Thread(target=self._send_results_threaded, args=(project_code, run_id_for_thread, results_to_send))
            send_thread.start()
        else:
            self.logger.log(f"No results to send for project {project_code} after filtering", "info")
        
        # Clear results regardless of filtering
        self.project_results[project_code] = []

    def _send_results(self) -> None:
        """Send results for all projects."""
        for project_code in self.project_configs.keys():
            self._send_results_for_project(project_code)

    def set_run_id(self, project_code: str, run_id: Union[str, int]) -> None:
        """Set run_id for a specific project."""
        if project_code in self.project_runs:
            self.project_runs[project_code] = int(run_id) if isinstance(run_id, str) else run_id
        else:
            self.logger.log(f"Unknown project code: {project_code}", "warning")

    def start_run(self) -> Dict[str, int]:
        """
        Create or verify test runs for all projects.
        
        :return: Dictionary mapping project codes to run IDs (as integers)
        """
        for project_code, project_data in self.project_configs.items():
            run_id = project_data.get('run_id')
            plan_id = project_data.get('plan_id')
            run_title = project_data.get('run_title')
            run_description = project_data.get('run_description')
            environment_id = project_data.get('environment')

            # If run_id is already set, verify it exists
            if run_id:
                run_id_int = int(run_id) if isinstance(run_id, str) else run_id
                if not self.client.check_test_run(project_code, run_id_int):
                    raise ReporterException(f"Unable to find given test run {run_id_int} for project {project_code}.")
                self.project_runs[project_code] = run_id_int
                continue

            # Create new test run
            if plan_id:
                created_run_id = self.client.create_test_run(
                    project_code=project_code,
                    title=run_title,
                    description=run_description,
                    plan_id=plan_id,
                    environment_id=environment_id
                )
            else:
                created_run_id = self.client.create_test_run(
                    project_code=project_code,
                    title=run_title,
                    description=run_description,
                    environment_id=environment_id
                )
            
            # Store run_id as int (API expects int)
            self.project_runs[project_code] = int(created_run_id) if isinstance(created_run_id, str) else created_run_id
            self.logger.log_debug(f"Created test run {self.project_runs[project_code]} for project {project_code}")

        return self.project_runs.copy()

    def complete_run(self) -> None:
        """Complete all test runs for all projects."""
        # Send remaining results for all projects
        if any(len(results) > 0 for results in self.project_results.values()):
            self._send_results()

        # Wait for all send operations to complete
        while self.count_running_threads > 0:
            pass

        # Complete all test runs
        for project_code, project_data in self.project_configs.items():
            if project_data.get('complete_after_run'):
                run_id = self.project_runs.get(project_code)
                if run_id:
                    self.logger.log_debug(f"Completing run {run_id} for project {project_code}")
                    self.client.complete_run(project_code, int(run_id))
                    self.logger.log_debug(f"Run {run_id} completed for project {project_code}")

                    # Enable public report if configured
                    if self.config.testops.show_public_report_link:
                        try:
                            self.logger.log_debug(f"Enabling public report for project {project_code}")
                            public_url = self.client.enable_public_report(project_code, int(run_id))
                            if public_url:
                                self.logger.log(f"Public report link for {project_code}: {public_url}", "info")
                            else:
                                self.logger.log(f"Failed to generate public report link for {project_code}", "warning")
                        except Exception as e:
                            self.logger.log(f"Failed to generate public report link for {project_code}: {e}", "warning")

    def complete_worker(self) -> None:
        """Complete worker - send remaining results."""
        if any(len(results) > 0 for results in self.project_results.values()):
            self._send_results()
        while self.count_running_threads > 0:
            pass
        self.logger.log_debug("Worker completed")

    def add_result(self, result: Result) -> None:
        """
        Add result to appropriate projects based on project mapping.
        
        :param result: Test result to add
        """
        # Get project mapping from result
        project_mapping = result.get_testops_project_mapping()

        if not project_mapping:
            # If no mapping, use default project or first project from config
            default_project = self.multi_config.default_project
            if not default_project and self.multi_config.projects:
                # Use first project from config if default_project is not specified
                default_project = self.multi_config.projects[0].code
                self.logger.log_debug(f"No default_project specified, using first project: {default_project}")
            
            if default_project:
                testops_ids = result.get_testops_ids() or []
                # Send result even if no testops_ids (test without ID)
                project_mapping = {default_project: testops_ids}
            else:
                self.logger.log(f"No project mapping and no projects configured for result {result.title}", "warning")
                return

        # Process result for each project in mapping
        for project_code, testops_ids in project_mapping.items():
            if project_code not in self.project_configs:
                self.logger.log(f"Unknown project {project_code} for result {result.title}, skipping", "warning")
                continue

            # Allow results without testops_ids (tests without IDs)
            # if not testops_ids:
            #     self.logger.log_debug(f"No testops_ids for project {project_code} in result {result.title}, skipping")
            #     continue

            # Create project-specific result
            project_result = self._create_project_result(result, project_code, testops_ids)

            # Show link for failed tests (only if testops_ids are present)
            if project_result.get_status() == 'failed' and testops_ids:
                self.__show_link(project_code, testops_ids, project_result.title)

            # Add to project queue
            self.project_results[project_code].append(project_result)

            # Check batch size and send if needed
            if len(self.project_results[project_code]) >= self.batch_size:
                self._send_results_for_project(project_code)

    def get_results(self) -> Dict[str, List[Result]]:
        """Get all results (pending + processed) grouped by project."""
        all_results = {}
        for project_code in self.project_configs.keys():
            all_results[project_code] = self.project_results[project_code] + self.processed[project_code]
        return all_results

    def set_results(self, results: Dict[str, List[Result]]) -> None:
        """Set results for projects."""
        for project_code, project_results in results.items():
            if project_code in self.project_results:
                self.project_results[project_code] = project_results

    def __show_link(self, project_code: str, ids: Union[None, List[int]], title: str):
        """Show link to failed test."""
        link = self.__prepare_link(project_code, ids, title)
        self.logger.log(f"See why this test failed: {link}", "info")

    def __prepare_link(self, project_code: str, ids: Union[None, List[int]], title: str):
        """Prepare link to test in Qase."""
        run_id = self.project_runs.get(project_code, '')
        # Ensure run_id is converted to string for URL
        run_id_str = str(run_id) if run_id else ''
        link = f"{self.__baseUrl}/run/{project_code}/dashboard/{run_id_str}?source=logs&search="
        if ids is not None and len(ids) > 0:
            return f"{link}{project_code}-{ids[0]}"
        return f"{link}{urllib.parse.quote_plus(title)}"

    @staticmethod
    def __get_host(host: str):
        """Get host URL for Qase."""
        if host == 'qase.io':
            return 'https://app.qase.io'
        return f'https://{host.replace("api", "app")}'
