import logging
import pathlib
import re
import uuid

from filelock import FileLock
from qase.commons import ConfigManager
from qase.commons.models import Result, Step, Field, Relation
from qase.commons.models.relation import SuiteData
from qase.commons.models.step import StepType, StepGherkinData
from qase.commons.reporters import QaseCoreReporter
from robot.libraries.BuiltIn import BuiltIn
from qase.commons.utils import QaseUtils

from .filter import Filter
from .plugin import QaseRuntimeSingleton
from .tag_parser import TagParser
from .types import STATUSES
from .models import *


def get_pool_id():
    return BuiltIn().get_variable_value('${PABOTQUEUEINDEX}', None)


def get_last_level_flag():
    return BuiltIn().get_variable_value('${PABOTISLASTEXECUTIONINPOOL}', None)


class Listener:
    ROBOT_LISTENER_API_VERSION = 3

    meta_run_file = pathlib.Path("src.run")

    def __init__(self):
        config = ConfigManager()
        self.reporter = QaseCoreReporter(
            config, 'robotframework', 'qase-robotframework')
        self.runtime = QaseRuntimeSingleton.get_instance()
        self.tests = {}
        self.pabot_index = None
        self.last_level_flag = None

        # Use centralized logger from config
        self.logger = config.logger

    def start_suite(self, suite, result):
        self.pabot_index = get_pool_id()
        self.last_level_flag = get_last_level_flag()
        if self.pabot_index is not None:
            try:
                if int(self.pabot_index) == 0:
                    test_run_id = self.reporter.start_run()
                    with FileLock("qase.lock"):
                        if test_run_id:
                            with open(self.meta_run_file, "w") as lock_file:
                                lock_file.write(str(test_run_id))
                else:
                    while True:
                        if Listener.meta_run_file.exists():
                            self.__load_run_from_lock()
                            break
            except RuntimeError:
                self.logger.log_error("Failed to create or read lock file")
        else:
            self.reporter.start_run()

        execution_plan = self.reporter.get_execution_plan()
        if execution_plan:
            selector = Filter(*execution_plan)
            suite.visit(selector)

        self.tests.update(self.__extract_tests_with_suites(suite))

    def start_test(self, test, result):
        self.logger.log_debug(f"Starting test '{test.name}'")

        self.runtime.result = Result(title=test.name, signature=test.name)
        self.runtime.steps = {}

    def end_user_keyword(self, data, implementation, result):
        self.logger.log_debug(f"Ending user keyword '{data.name}'")

        test_metadata = TagParser.parse_tags(result.tags, self.logger)

        if test_metadata.params:
            # Get argument names from the implementation
            args_names = implementation.args.argument_names if hasattr(
                implementation.args, 'argument_names') else []
            args_values = result.args if hasattr(result, 'args') else []
            params: dict = {}
            for param in test_metadata.params:
                if param in args_names:
                    params[param] = args_values[args_names.index(param)]
            self.runtime.result.params = params

        if test_metadata.fields:
            for key, value in test_metadata.fields.items():
                self.runtime.result.add_field(Field(key, value))

    def end_test(self, test, result):
        self.logger.log_debug(f"Finishing test '{test.name}'")

        test_metadata = TagParser.parse_tags(test.tags, self.logger)

        if test_metadata.ignore:
            self.logger.log_info(f"Test '{test.name}' is ignored")
            return

        if test_metadata.qase_multi_ids:
            # Multi-project mode: set project mapping
            for project_code, testops_ids in test_metadata.qase_multi_ids.items():
                self.runtime.result.set_testops_project_mapping(project_code, testops_ids)
        elif test_metadata.qase_ids:
            # Single project mode: use old testops_ids
            self.runtime.result.testops_ids = test_metadata.qase_ids

        self.runtime.result.execution.complete()

        # Determine if it's an assertion error or other error
        status = STATUSES[result.status]
        if status == "failed" and hasattr(result, 'message'):
            # Check if the error message contains assertion-related keywords
            assertion_keywords = ['assert', 'AssertionError',
                                  'expect', 'should', 'must', 'equal', 'not equal']
            is_assertion_error = any(
                keyword in result.message for keyword in assertion_keywords)
            status = "failed" if is_assertion_error else "invalid"

        self.runtime.result.execution.set_status(status)
        if hasattr(result, 'message'):
            self.runtime.result.execution.stacktrace = result.message

        steps = self.__parse_steps(result)
        self.runtime.result.add_steps(steps)

        # Process parameters if they exist
        if test_metadata.params:
            for param in test_metadata.params:
                param_value = BuiltIn().get_variable_value(f"${{{param}}}")
                if param_value is not None:
                    self.runtime.result.add_param(param, param_value)

        if hasattr(test, "doc"):
            self.runtime.result.add_field(Field("description", test.doc))

        if test_metadata.fields:
            for key, value in test_metadata.fields.items():
                self.runtime.result.add_field(Field(key, value))

        suites = self.tests.get(f"{test.name}:{test.lineno}")
        if suites:
            relations = Relation()
            for suite in suites:
                relations.add_suite(SuiteData(suite))
            self.runtime.result.relations = relations

            self.runtime.result.signature = QaseUtils.get_signature(
                self.runtime.result.testops_ids,
                [suite.lower().replace(" ", "_") for suite in suites] +
                [test.name.lower().replace(" ", "_")],
                self.runtime.result.params
            )

        self.reporter.add_result(self.runtime.result)

        self.logger.log_info(
            f"Finished case result: {result.status}, error: {hasattr(result, 'message') and result.message or None}"
        )

    def close(self):
        if self.last_level_flag is not None:
            if int(self.last_level_flag) == 1:
                Listener.drop_run_id()
            else:
                self.reporter.complete_worker()

        if not Listener.meta_run_file.exists():
            self.logger.log_info("complete run executing")
            self.reporter.complete_run()

    def __extract_tests_with_suites(self, suite, parent_suites=None):
        if parent_suites is None:
            parent_suites = []

        current_suites = parent_suites + [suite.name]

        test_dict = {}

        if hasattr(suite, 'suites') and suite.suites:
            for sub_suite in suite.suites:
                test_dict.update(self.__extract_tests_with_suites(
                    sub_suite, current_suites))

        if hasattr(suite, 'tests') and suite.tests:
            for test in suite.tests:
                test_key = f"{test.name}:{test.lineno}"
                test_dict[test_key] = current_suites

        return test_dict

    def __extract_resolved_variables(self, body_element, accumulated_vars: dict = None) -> dict:
        """
        Extract resolved variable values from log messages in the body element.
        Robot Framework logs variable assignments in format: ${variable} = value
        Returns a dictionary mapping variable names to their resolved values.
        Accumulates variables from all nested messages recursively.
        """
        if accumulated_vars is None:
            accumulated_vars = {}
        
        if not hasattr(body_element, "body"):
            return accumulated_vars
        
        # Pattern to match variable assignments: ${variable} = value
        # This matches patterns like: ${full_url} = https://jsonplaceholder.typicode.com/users
        # Also handles nested variables like ${response.status_code}
        # The pattern captures everything after '=' until end of line or next variable assignment
        var_pattern = re.compile(r'\$\{([^}]+)\}\s*=\s*(.+?)(?=\s+\$\{|$)')
        
        # Also try to extract from BuiltIn API for variables that might not be in messages
        try:
            builtin = BuiltIn()
        except Exception:
            builtin = None
        
        for item in body_element.body:
            if hasattr(item, "type") and item.type == "MESSAGE":
                # Try different possible attributes for message content
                message_text = None
                if hasattr(item, "message"):
                    message_text = str(item.message)
                elif hasattr(item, "msg"):
                    message_text = str(item.msg)
                elif hasattr(item, "text"):
                    message_text = str(item.text)
                
                if message_text:
                    # Try to match variable assignment pattern
                    match = var_pattern.search(message_text)
                    if match:
                        var_name = match.group(1)
                        var_value = match.group(2).strip()
                        # Remove trailing commas, semicolons, or other punctuation that might be captured
                        var_value = var_value.rstrip(',;')
                        # Store both with and without ${} for flexible matching
                        accumulated_vars[var_name] = var_value
                        accumulated_vars[f"${{{var_name}}}"] = var_value
                        # Also handle nested variable access like response.status_code
                        if '.' in var_name:
                            parts = var_name.split('.')
                            base_var = parts[0]
                            accumulated_vars[f"${{{base_var}}}"] = var_value  # Store base variable too
                    
                    # Also try to extract variable names mentioned in the message
                    # and resolve them via BuiltIn API if available
                    if builtin:
                        # Find all variable references in the message
                        var_refs = re.findall(r'\$\{([^}]+)\}', message_text)
                        for var_ref in var_refs:
                            if var_ref not in accumulated_vars and f"${{{var_ref}}}" not in accumulated_vars:
                                try:
                                    var_value = builtin.get_variable_value(f"${{{var_ref}}}")
                                    if var_value is not None:
                                        accumulated_vars[var_ref] = str(var_value)
                                        accumulated_vars[f"${{{var_ref}}}"] = str(var_value)
                                except Exception:
                                    pass
            
            # Recursively process nested body elements to accumulate variables
            if hasattr(item, "body") and item.body:
                self.__extract_resolved_variables(item, accumulated_vars)
        
        return accumulated_vars

    def __resolve_variables_in_data(self, data: str, resolved_vars: dict) -> str:
        """
        Replace variable placeholders in data string with their resolved values.
        Uses regex to match variable patterns and replace them with resolved values.
        Aggressively uses BuiltIn API to resolve any remaining variables.
        """
        if not data:
            return data
        
        result = data
        # Sort by length (longest first) to handle nested variables correctly
        sorted_vars = sorted(resolved_vars.items(), key=lambda x: len(x[0]), reverse=True)
        
        for var_placeholder, var_value in sorted_vars:
            # Replace all occurrences of the variable placeholder
            # Use regex to match exact variable patterns (e.g., ${var} but not ${var_suffix})
            if var_placeholder.startswith('${') and var_placeholder.endswith('}'):
                # Escape special regex characters in the variable name
                escaped_var = re.escape(var_placeholder)
                # Match the variable as a whole word/pattern
                pattern = re.compile(escaped_var)
                result = pattern.sub(str(var_value), result)
            else:
                # For non-brace variables, use simple string replacement
                result = result.replace(var_placeholder, str(var_value))
        
        # Aggressively try to resolve any remaining variables using BuiltIn API
        # This handles cases where variables weren't captured in messages,
        # including object attributes like response.status_code
        try:
            builtin = BuiltIn()
            
            # Find all ${variable} patterns (scalar variables)
            scalar_vars = re.findall(r'\$\{([^}]+)\}', result)
            for var_name in scalar_vars:
                # Skip if already resolved
                if var_name in resolved_vars or f"${{{var_name}}}" in resolved_vars:
                    continue
                
                try:
                    # Handle cases like ${<Response [200]>.status_code} or ${response.status_code}
                    if '.' in var_name and ('<' in var_name or '>' in var_name or not var_name.startswith('<')):
                        # This is an object attribute access
                        # Pattern: ${<Object [info]>.attribute} or ${object.attribute}
                        parts = var_name.split('.')
                        # Remove angle brackets and brackets if present from base name
                        base_name = parts[0].strip('<>[]').strip()
                        # Remove any text in brackets like [200]
                        base_name = re.sub(r'\[.*?\]', '', base_name).strip()
                        
                        # Try to get base variable
                        base_value = builtin.get_variable_value(f"${{{base_name}}}")
                        if base_value is not None:
                            # Try to get nested attribute
                            current = base_value
                            for attr in parts[1:]:
                                if hasattr(current, attr):
                                    current = getattr(current, attr)
                                elif isinstance(current, dict) and attr in current:
                                    current = current[attr]
                                elif hasattr(current, '__getitem__'):
                                    try:
                                        current = current[attr]
                                    except (KeyError, TypeError, IndexError):
                                        current = None
                                        break
                                else:
                                    current = None
                                    break
                            
                            if current is not None:
                                result = result.replace(f"${{{var_name}}}", str(current))
                                continue
                    
                    # Try to get variable value normally
                    var_value = builtin.get_variable_value(f"${{{var_name}}}")
                    if var_value is not None:
                        # Replace all occurrences
                        result = result.replace(f"${{{var_name}}}", str(var_value))
                except Exception:
                    # If variable resolution fails, try alternative approaches
                    if '.' in var_name:
                        try:
                            # Try to split and resolve nested attributes
                            parts = var_name.split('.')
                            # Remove angle brackets and brackets if present
                            base_name = parts[0].strip('<>[]').strip()
                            # Remove any text in brackets
                            base_name = re.sub(r'\[.*?\]', '', base_name).strip()
                            
                            # Try to get base variable
                            base_value = builtin.get_variable_value(f"${{{base_name}}}")
                            if base_value is not None:
                                # Try to get nested attribute
                                current = base_value
                                for attr in parts[1:]:
                                    if hasattr(current, attr):
                                        current = getattr(current, attr)
                                    elif isinstance(current, dict) and attr in current:
                                        current = current[attr]
                                    elif hasattr(current, '__getitem__'):
                                        try:
                                            current = current[attr]
                                        except (KeyError, TypeError, IndexError):
                                            current = None
                                            break
                                    else:
                                        current = None
                                        break
                                
                                if current is not None:
                                    result = result.replace(f"${{{var_name}}}", str(current))
                        except Exception:
                            pass
            
            # Find all @{variable} patterns (list variables)
            list_vars = re.findall(r'@\{([^}]+)\}', result)
            for var_name in list_vars:
                try:
                    var_value = builtin.get_variable_value(f"@{{{var_name}}}")
                    if var_value is not None:
                        # Convert list to string representation
                        if isinstance(var_value, (list, tuple)):
                            list_str = ', '.join(str(item) for item in var_value)
                            result = result.replace(f"@{{{var_name}}}", list_str)
                        else:
                            result = result.replace(f"@{{{var_name}}}", str(var_value))
                except Exception:
                    pass
            
            # Also handle &{variable} patterns (dictionary variables)
            dict_vars = re.findall(r'&\{([^}]+)\}', result)
            for var_name in dict_vars:
                try:
                    var_value = builtin.get_variable_value(f"&{{{var_name}}}")
                    if var_value is not None:
                        result = result.replace(f"&{{{var_name}}}", str(var_value))
                except Exception:
                    pass
                    
        except Exception:
            # If BuiltIn is not available or fails, continue with what we have
            pass
        
        return result

    def __parse_steps(self, result, accumulated_vars: dict = None) -> List[Step]:
        """
        Parse test steps from Robot Framework result, resolving variable values.
        Accumulates resolved variables from all previous steps to resolve variables
        in subsequent steps.
        """
        if accumulated_vars is None:
            accumulated_vars = {}
        
        steps = []

        for i in range(len(result.body)):
            if hasattr(result.body[i], "type") and result.body[i].type == "MESSAGE":
                continue

            if hasattr(result.body[i], "type") and result.body[i].type == "IF/ELSE ROOT":
                condition_steps = self.__parse_condition_steps(result.body[i], accumulated_vars.copy())
                for step in condition_steps:
                    steps.append(step)
                continue

            if hasattr(result.body[i], "type") and result.body[i].type != "KEYWORD":
                step_name = result.body[i].type
                if hasattr(result.body[i], "values"):
                    step_name += " " + " ".join(result.body[i].values)
            else:
                step_name = result.body[i].name

            data = None
            # Avoid deprecated args attribute for For and ForIteration objects
            # Check class name to identify For/ForIteration objects and use values instead
            body_element = result.body[i]
            class_name = body_element.__class__.__name__
            
            # For and ForIteration objects have deprecated args attribute
            # Use values attribute instead for these types
            if class_name in ('For', 'ForIteration'):
                if hasattr(body_element, "values") and body_element.values:
                    data = ' '.join(str(val) for val in body_element.values)
            else:
                # For other types, try to use args if available
                # Use getattr to avoid triggering deprecation warning on access
                try:
                    args_value = getattr(body_element, "args", None)
                    if args_value:
                        data = ' '.join(str(arg) for arg in args_value)
                except (AttributeError, TypeError):
                    # Fallback to values if args is not available
                    if hasattr(body_element, "values") and body_element.values:
                        data = ' '.join(str(val) for val in body_element.values)

            # Extract resolved variable values from log messages in this step
            # This will also accumulate variables from nested messages
            step_resolved_vars = self.__extract_resolved_variables(body_element, accumulated_vars.copy())
            
            # Merge newly resolved variables into accumulated variables
            accumulated_vars.update(step_resolved_vars)
            
            # Also try to resolve variables directly from BuiltIn API before resolving in data
            # This helps with variables that weren't logged but are available in the context
            if data:
                try:
                    builtin = BuiltIn()
                    # Find all variable patterns in data
                    all_vars = re.findall(r'[\$@&]\{([^}]+)\}', data)
                    for var_name in all_vars:
                        if var_name not in accumulated_vars and f"${{{var_name}}}" not in accumulated_vars:
                            try:
                                # Try scalar variable
                                var_value = builtin.get_variable_value(f"${{{var_name}}}")
                                if var_value is not None:
                                    accumulated_vars[var_name] = str(var_value)
                                    accumulated_vars[f"${{{var_name}}}"] = str(var_value)
                            except Exception:
                                try:
                                    # Try list variable
                                    var_value = builtin.get_variable_value(f"@{{{var_name}}}")
                                    if var_value is not None:
                                        if isinstance(var_value, (list, tuple)):
                                            var_str = ', '.join(str(item) for item in var_value)
                                        else:
                                            var_str = str(var_value)
                                        accumulated_vars[var_name] = var_str
                                        accumulated_vars[f"@{{{var_name}}}"] = var_str
                                except Exception:
                                    pass
                except Exception:
                    pass
            
            # Resolve variables in data using all accumulated variables
            if data and accumulated_vars:
                data = self.__resolve_variables_in_data(data, accumulated_vars)

            step = Step(
                step_type=StepType.GHERKIN,
                id=str(uuid.uuid4()),
                data=StepGherkinData(
                    keyword=step_name, name=step_name, line=0, data=data)
            )

            # Determine step status
            step_status = STATUSES[result.body[i].status]
            if step_status == "failed":
                # For steps, we'll use a simpler approach - check if it's a keyword failure
                # Robot Framework doesn't provide detailed error info for individual steps
                step_status = "failed"  # Keep as failed for steps, main test status is handled above
            step.execution.set_status(step_status)
            step.execution.start_time = result.body[i].start_time.timestamp()
            step.execution.duration = result.body[i].elapsed_time.microseconds
            step.execution.end_time = result.body[i].end_time.timestamp()

            if hasattr(result.body[i], "body"):
                # Recursively parse nested steps, passing accumulated variables
                step.steps = self.__parse_steps(result.body[i], accumulated_vars.copy())

            steps.append(step)

        return steps

    def __parse_condition_steps(self, result_step, accumulated_vars: dict = None) -> List[Step]:
        if accumulated_vars is None:
            accumulated_vars = {}
        
        steps = []

        for body_element in result_step.body:
            if hasattr(body_element, "type"):
                step = Listener._create_gherkin_step_with_type(body_element)
                child_steps = self.__parse_steps(body_element, accumulated_vars.copy())

                Listener._set_step_status_based_on_children(step, child_steps)
                step.steps = child_steps
            else:
                step = Listener._create_gherkin_step_from_name(body_element)

            step.execution.start_time = None
            step.execution.end_time = None

            steps.append(step)

        return steps

    @staticmethod
    def _create_gherkin_step_with_type(body_element) -> Step:
        """Create a Gherkin step from a body element with type attribute."""
        step = Step(
            step_type=StepType.GHERKIN,
            id=str(uuid.uuid4()),
            data=StepGherkinData(
                keyword=body_element.type,
                name=body_element.type,
                line=0
            )
        )

        return step

    @staticmethod
    def _create_gherkin_step_from_name(body_element) -> Step:
        """Create a Gherkin step from a body element with name attribute."""
        step = Step(
            step_type=StepType.GHERKIN,
            id=str(uuid.uuid4()),
            data=StepGherkinData(
                keyword=body_element.name,
                name=body_element.name,
                line=0
            )
        )

        return step

    @staticmethod
    def _set_step_status_based_on_children(step: Step, child_steps: List[Step]) -> None:
        """Set the status of a step based on its children's statuses."""
        if all(s.execution.status == "skipped" for s in child_steps):
            step.execution.set_status("skipped")
        else:
            step.execution.set_status("passed")

    def __load_run_from_lock(self):
        if Listener.meta_run_file.exists():
            with open(Listener.meta_run_file, "r") as lock_file:
                try:
                    test_run_id = str(lock_file.read())
                    self.reporter.set_run_id(test_run_id)
                except ValueError:
                    pass

    @staticmethod
    def drop_run_id():
        if Listener.meta_run_file.exists():
            Listener.meta_run_file.unlink()
