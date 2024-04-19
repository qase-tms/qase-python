import uuid
from typing import Tuple, Union

import pytest

from .plugin import PluginNotInitializedException, QasePytestPluginSingleton
from qase.commons.models.step import Step, StepTextData, StepType

from .context_manager import contextdecorator


class qase:
    """Class with decorators for pytest"""

    @staticmethod
    def id(id):
        """
        Define a persisent connection to Qase TestOps test case.

        >>> @qase.id(1)
        >>> def test_example():
        >>>     pass

        :param id: int id of test case
        :return: pytest.mark instance
        """
        return pytest.mark.qase_id(id=id)

    @staticmethod
    def title(title):
        """
        >>> @qase.title("Sign up")
        >>> def test_example():
        >>>     pass

        :param title: a string with test name
        :return: pytest.mark instance
        """
        return pytest.mark.qase_title(title=title)

    @staticmethod
    def fields(*fields: Tuple[str, str]):
        """
        >>> @qase.fields(
                ("priority", "high"),
                ("layer", "API")
                ("custom_field", "custom_value")
            )
        >>> def test_example():
        >>>     pass

        :param name: a string with field name
        :param value: a string with field value
        :return: pytest.mark instance
        """
        return pytest.mark.qase_fields(fields=fields)

    @staticmethod
    def suite(title: str, description: str = None):
        """
        >>> @qase.suite("Sign up")
        >>> def test_example():
        >>>     pass

        :param title: a string with suite name. You can use dot notation to create nested suites.
        :param description: a string with suite description
        :return: pytest.mark instance
        """
        return pytest.mark.qase_suite(title=title, description=description)

    @staticmethod
    def author(author):
        """
        >>> @qase.author("John Doe")
        >>> def test_example():
        >>>     pass

        :param author: a string with test author
        :return: pytest.mark instance
        """
        return pytest.mark.qase_author(author=author)

    @staticmethod
    def description(description):
        """
        >>> @qase.description("Sign up user using login and password")
        >>> def test_example():
        >>>     pass

        :param description: a string with test full description. Markdown is supported.
        :return: pytest.mark instance
        """
        return pytest.mark.qase_description(description=description)

    @staticmethod
    def preconditions(preconditions):
        """
        >>> @qase.preconditions("Sign up user using login and password")
        >>> def test_example():
        >>>     pass

        :param preconditions: a string with test preconditions. Markdown is supported.
        :return: pytest.mark instance
        """
        return pytest.mark.qase_preconditions(preconditions=preconditions)

    @staticmethod
    def postconditions(postconditions):
        """
        >>> @qase.postconditions("Sign up user using login and password")
        >>> def test_example():
        >>>     pass

        :param postconditions: a string with test postconditions. Markdown is supported.
        :return: pytest.mark instance
        """
        return pytest.mark.qase_postconditions(postconditions=postconditions)

    @staticmethod
    def severity(severity):
        """
        >>> @qase.severity("critical")
        >>> def test_example():
        >>>     pass

        :param severity: a string with test severity. Default values: blocker, critical, major, normal, minor, trivial.
        :return: pytest.mark instance
        """
        return pytest.mark.qase_severity(severity=severity)

    @staticmethod
    def priority(priority):
        """
        >>> @qase.priority("Critical")
        >>> def test_example():
        >>>     pass

        :param priority: a string with test priority. Default values: low, medium, high.
        :return: pytest.mark instance
        """
        return pytest.mark.qase_priority(priority=priority)

    @staticmethod
    def layer(layer):
        """
        >>> @qase.layer("E2E")
        >>> def test_example():
        >>>     pass

        :param layer: a string with test layer. Default values: E2E, API, Unit.
        :return: pytest.mark instance
        """
        return pytest.mark.qase_layer(layer=layer)

    @staticmethod
    def tags(*tags):
        """
        >>> @qase.tags("tag1", "tag2")
        >>> def test_example():
        >>>     pass

        :param tags: a list of strings with test tags.
        :return: pytest.mark instance
        """
        return pytest.mark.qase_tags(tags=tags)

    @staticmethod
    def ignore():
        """
        >>> @qase.ignore()
        >>> def test_example():
        >>>     pass

        :return: pytest.mark instance
        """
        return pytest.mark.qase_ignore()

    @staticmethod
    def muted():
        """
        >>> @qase.muted()
        >>> def test_example():
        >>>     pass

        :return: pytest.mark instance
        """
        return pytest.mark.qase_muted()

    @staticmethod
    def attach(*files: Union[str, Tuple[str, str], Tuple[bytes, str, str]]):
        """
        Attach files to test results

        `files` could be:
            - str - only `filepath`
            - str, str - `filepath` and `mime-type` for it
            - bytes, str, str - `source` data, `mime-type` and `filename`

        >>> from src.client.models import MimeTypes
        ... qase.attach(
        ...     (driver.get_screenshot_as_png(), MimeTypes.PNG, "page.png")
        ... )
        """
        try:
            plugin = QasePytestPluginSingleton.get_instance()
            plugin.add_attachments(*files)
        except Exception:
            print("Failed to add attachments")
            pass

    @staticmethod
    @contextdecorator
    def step(title, expected=None):
        """
        Step context/decorator

        Usage:

        >>> @qase.step("First step")
        ... def first_step():
        ...     print("smthng")

        >>> with qase.step("Second step"):
        ...     print("smthng")
        """
        plugin = None
        id = str(uuid.uuid4())
        try:
            plugin = QasePytestPluginSingleton.get_instance()
            step = Step(
                step_type=StepType.TEXT,
                id=id,
                data=StepTextData(
                    action=title,
                    expected_result=expected if expected else None,
                )
            )
            plugin.start_step(step)
            yield
            plugin.finish_step(id=step.id)
        except PluginNotInitializedException:
            yield
        except AttributeError:
            yield
        except Exception as e:
            plugin.finish_step(id=id, exception=e)
            raise e
