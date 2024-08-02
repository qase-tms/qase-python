from qase.commons.models.runtime import Runtime


class QaseRuntimeSingleton:
    _instance: Runtime = None

    @staticmethod
    def get_instance() -> Runtime:
        """ Static access method"""
        if QaseRuntimeSingleton._instance is None:
            QaseRuntimeSingleton._instance = Runtime()
        return QaseRuntimeSingleton._instance

    def __init__(self):
        """ Virtually private constructor"""
        raise Exception("Use get_instance()")
