from ..basemodel import BaseModel


class ApiConfig(BaseModel):
    token: str = None
    host: str = None
    timeout: int = None
    retries: int = None
    retry_backoff: int = None

    def __init__(self):
        self.host = "qase.io"
        self.timeout = 30
        self.retries = 3
        self.retry_backoff = 2

    def set_token(self, token: str):
        self.token = token

    def set_host(self, host: str):
        self.host = host

    def set_timeout(self, timeout: int):
        timeout = int(timeout)
        if timeout <= 0:
            raise ValueError("API timeout should be greater than 0")
        self.timeout = timeout

    def set_retries(self, retries: int):
        retries = int(retries)
        if retries < 0:
            raise ValueError("API retries should be 0 or greater")
        self.retries = retries

    def set_retry_backoff(self, retry_backoff: int):
        retry_backoff = int(retry_backoff)
        if retry_backoff < 0:
            raise ValueError("API retry backoff should be 0 or greater")
        self.retry_backoff = retry_backoff
