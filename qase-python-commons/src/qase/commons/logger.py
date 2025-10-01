import os
import datetime
import threading
from typing import Optional


class LoggingOptions:
    def __init__(self, console: bool = True, file: bool = False):
        self.console = console
        self.file = file


class Logger:
    _log_file = None

    def __init__(self, debug: bool = False, prefix: str = '', dir: str = os.path.join('.', 'logs'), 
                 logging_options: Optional[LoggingOptions] = None) -> None:
        self.debug = debug
        self.prefix = prefix
        self.dir = dir
        
        # Initialize logging options
        if logging_options is None:
            # Default behavior: console always enabled, file enabled only in debug mode
            self.logging_options = LoggingOptions(
                console=True,
                file=debug
            )
        else:
            self.logging_options = logging_options
        
        # Override with environment variables if set
        self._load_env_logging_options()
        
        # Setup file logging if enabled
        if self.logging_options.file:
            if Logger._log_file is None:
                timestamp = self._get_timestamp()
                filename = f'{prefix}_{timestamp}.log'
                if not os.path.exists(dir):
                    os.makedirs(dir)
                Logger._log_file = os.path.join(dir, filename)

            with open(Logger._log_file, 'a', encoding='utf-8'):
                pass

            self.lock = threading.Lock()

    def _load_env_logging_options(self):
        """Load logging options from environment variables"""
        # QASE_LOGGING_CONSOLE
        console_env = os.environ.get('QASE_LOGGING_CONSOLE')
        if console_env is not None:
            self.logging_options.console = console_env.lower() in ('true', '1', 'yes', 'on')
        
        # QASE_LOGGING_FILE
        file_env = os.environ.get('QASE_LOGGING_FILE')
        if file_env is not None:
            self.logging_options.file = file_env.lower() in ('true', '1', 'yes', 'on')
        
        # Legacy QASE_DEBUG support
        debug_env = os.environ.get('QASE_DEBUG')
        if debug_env is not None and debug_env.lower() in ('true', '1', 'yes', 'on'):
            # When debug is enabled via env, enable file logging if not explicitly disabled
            if not hasattr(self.logging_options, 'file') or self.logging_options.file is None:
                self.logging_options.file = True

    def log(self, message: str, level: str = 'info'):
        time_str = self._get_timestamp("%H:%M:%S")
        log = f"[Qase][{time_str}][{level}] {message}\n"

        # Console output
        if self.logging_options.console:
            try:
                print(log, end='')
            except (OSError, IOError):
                pass

        # File output
        if self.logging_options.file:
            with self.lock:
                with open(Logger._log_file, 'a', encoding='utf-8') as f:
                    f.write(log)

    def log_debug(self, message: str):
        if self.debug:
            self.log(message, 'debug')

    def log_error(self, message: str):
        self.log(message, 'error')

    def log_warning(self, message: str):
        self.log(message, 'warning')

    def log_info(self, message: str):
        self.log(message, 'info')

    @staticmethod
    def _get_timestamp(fmt: str = "%Y%m%d"):
        now = datetime.datetime.now()
        return now.strftime(fmt)
