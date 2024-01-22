import json
import os
import requests


class WebApi:
    """
    Api that is used by Web client.
    Qase api differs from web api and doesn't cover all features that are accessible through web api.

    It is required to specify env variables:
    QASE_WEB_SRF_TOKEN, QASE_WEB_HOST_SESSION, QASE_WEB_SESSION (balancing-cookie)
    """

    def __init__(self):
        srf_token = os.getenv("QASE_WEB_SRF_TOKEN")
        if not srf_token:
            raise EnvironmentError("Set environment variable QASE_WEB_SRF_TOKEN")
        host_session = os.getenv("QASE_WEB_HOST_SESSION")
        if not host_session:
            raise EnvironmentError("Set environment variable QASE_WEB_HOST_SESSION")
        balancing_cookie = os.getenv("QASE_WEB_SESSION")
        if not balancing_cookie:
            raise EnvironmentError("Set environment variable QASE_WEB_SESSION")

        self.cookies = {
            "XSRF-TOKEN": srf_token,
            "__Host-session": host_session,
            "balancing-cookie": balancing_cookie
        }
        self.api_url = "https://app.qase.io/v1/"

    def get_session_data(self, email, password):
        """Get session data that is cached in cookies"""
        headers = {"Content-Type": "application/json"}
        req_data = {"email": email, "password": password, "remember": True}
        url = "https://app.qase.io/v1/auth/login/regular"
        with requests.post(url, headers=headers, data=json.dumps(req_data)) as response:
            cookies = response.cookies.get_dict()
            web_session_name = next((cookie for cookie, value in cookies.items() if cookie.startswith("remember_web_")), None)
            if not web_session_name:
                web_session_name = "balancing-cookie"
            return (cookies["XSRF-TOKEN"], cookies["__Host-session"], {web_session_name: cookies[web_session_name]})

    @staticmethod
    def get_content(response):
        return json.loads(response.content.decode("UTF-8"))

    def get(self, uri):
        url = self.api_url + uri
        with requests.get(url, cookies=self.cookies) as response:
            return self.get_content(response)

    def put(self, uri):
        raise NotImplementedError()

    def patch(self, uri):
        raise NotImplementedError()

    def delete(self, uri):
        raise NotImplementedError()
