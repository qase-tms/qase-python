from ..basemodel import BaseModel


class ApiConfig(BaseModel):
    token: str = None
    host: str = None

    def __init__(self):
        self.host = "qase.io"

    def set_token(self, token: str):
        self.token = token

    def set_host(self, host: str):
        self.host = host
