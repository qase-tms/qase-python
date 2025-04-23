import os
import datetime
import threading


class Logger:
    _log_file = None

    def __init__(self, debug: bool = False, prefix: str = '', dir: str = os.path.join('.', 'logs')) -> None:
        self.debug = debug
        if self.debug:
            if Logger._log_file is None:
                timestamp = self._get_timestamp()
                filename = f'{prefix}_{timestamp}.log'
                if not os.path.exists(dir):
                    os.makedirs(dir)
                Logger._log_file = os.path.join(dir, filename)

            with open(Logger._log_file, 'a', encoding='utf-8'):
                pass

            self.lock = threading.Lock()

    def log(self, message: str, level: str = 'info'):
        time_str = self._get_timestamp("%H:%M:%S")
        log = f"[Qase][{time_str}][{level}] {message}\n"

        try:
            print(log, end='')
        except (OSError, IOError):
            pass

        if self.debug:
            with self.lock:
                with open(Logger._log_file, 'a', encoding='utf-8') as f:
                    f.write(log)

    def log_debug(self, message: str):
        if self.debug:
            self.log(message, 'debug')

    @staticmethod
    def _get_timestamp(fmt: str = "%Y%m%d"):
        now = datetime.datetime.now()
        return now.strftime(fmt)
