from json import JSONDecodeError

from qaseio.utils.web.web_api import WebApi


class Web(WebApi):
    def get_run_info(self, project, run_id):
        try:
            return self.get(f"project/{project}/run/{run_id}/dashboard/info")
        except JSONDecodeError:
            raise EnvironmentError(
                "Update envs for cookie values: QASE_WEB_HOST_SESSION, QASE_WEB_SESSION and QASE_WEB_SRF_TOKEN"
            )
