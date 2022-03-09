import logging


class Logging:

    LOG_LEVEL = logging.INFO
    logger = None

    @staticmethod
    def set_logging_level(value):
        Logging.LOG_LEVEL = value
        Logging._setup_logging(Logging.LOG_LEVEL)

    @staticmethod
    def _setup_logging(log_level):
        """Setup basic logging

        Args:
          log_level (int): minimum loglevel for emitting messages
        """

        # Suppress overly verbose logs from libraries that aren't helpful
        if log_level == logging.DEBUG:
            logging.getLogger("requests").setLevel(logging.DEBUG)
            logging.getLogger("urllib3").setLevel(logging.DEBUG)
        else:
            logging.getLogger("requests").setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)

        Logging.logger = logging.getLogger("apitist")
        Logging.logger.setLevel(log_level)


Logging._setup_logging(Logging.LOG_LEVEL)
