from qaseio.utils.web.web_api import WebApi


class Web(WebApi):
    def get_run_info(self, project, run_id):
        return self.get(f"project/{project}/run/{run_id}/dashboard/info")
