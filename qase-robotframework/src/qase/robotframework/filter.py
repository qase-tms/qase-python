from robot.api import SuiteVisitor

from .tag_parser import TagParser


class Filter(SuiteVisitor):

    def __init__(self, *tests):
        self.tests = tests

    def start_suite(self, suite):
        suite.tests = [t for t in suite.tests if self._is_included(t)]

    def _is_included(self, test):
        test_metadata = TagParser.parse_tags(test.tags)

        if test_metadata.qase_ids:
            return any(qase_id in self.tests for qase_id in test_metadata.qase_ids)

        return False

    def end_suite(self, suite):
        suite.suites = [s for s in suite.suites if s.test_count > 0]

    def visit_test(self, test):
        pass
