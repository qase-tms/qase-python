import datetime

import os


class Logger:
    def __init__(self, debug: bool = False, prefix: str = '', dir: str = os.path.join('.', 'logs')) -> None:
        self.debug = debug
        if self.debug:
            filename = f'{prefix}_{self._get_timestamp()}.log'
            if not os.path.exists(dir):
                os.makedirs(dir)
            self.log_file = os.path.join(dir, f'{filename}')
            with open(self.log_file, 'w'):
                pass

    def log(self, message: str, level: str = 'info'):
        time_str = self._get_timestamp("%H:%M:%S")
        log = f"[Qase][{time_str}][{level}] {message}\n"
        print(log)
        if self.debug:
            with open(self.log_file, 'a') as f:
                f.write(log)

    def log_debug(self, message: str):
        if self.debug:
            self.log(message, 'debug')

    @staticmethod
    def _get_timestamp(format: str = "%Y%m%d_%H_%M_%S"):
        now = datetime.datetime.now()
        return now.strftime(format)
