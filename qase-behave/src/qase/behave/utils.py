import datetime
import json
import os
import time
import uuid
from typing import List

from behave.model import Scenario, Step
from qase.commons.models import Result, Relation
from qase.commons.models.relation import SuiteData
from qase.commons.models.step import StepType, StepGherkinData, Step as QaseStep
from qase.commons.utils import QaseUtils

SUITE = "suite"
IGNORE = "ignore"
FIELDS = "fields"
TESTOPS_ID = "testops_ids"
TESTOPS_PROJECT_ID = "testops_project_id"
TAGS = "tags"


def filter_scenarios(case_ids: List[int], scenarios: List[Scenario]) -> List[Scenario]:
    if not case_ids:
        return scenarios

    executed_scenarios = []
    for scenario in scenarios:
        tags = __parse_tags(scenario.tags)
        if TESTOPS_ID in tags:
            if any(qase_id in case_ids for qase_id in tags[TESTOPS_ID]):
                executed_scenarios.append(scenario)

    return executed_scenarios


def parse_scenario(scenario: Scenario, logger=None) -> Result:
    tags = __parse_tags(scenario.tags, logger)

    result = Result(scenario.name, scenario.name)

    # Check for project_id tags first (multi-project mode)
    project_ids = tags.get(TESTOPS_PROJECT_ID, None)
    if project_ids:
        # Multi-project mode: set project mapping
        for project_code, testops_ids in project_ids.items():
            result.set_testops_project_mapping(project_code, testops_ids)
    else:
        # Single project mode: use old testops_ids
        result.testops_ids = tags.get(TESTOPS_ID, None)
    
    result.fields = tags.get(FIELDS, {})
    result.ignore = tags.get(IGNORE, False)

    tag_list = tags.get(TAGS, [])
    if tag_list:
        result.add_tags(tag_list)

    relation = Relation()
    if SUITE in tags:
        for suite in tags[SUITE]:
            relation.suite.add_data(SuiteData(suite))
    else:
        suites = scenario.filename.split(os.sep)
        for suite in suites:
            relation.suite.add_data(SuiteData(suite))

    result.relations = relation

    result.params = __parse_parameters(scenario)

    result.execution.set_status("passed")
    
    result.signature = QaseUtils.get_signature(
        result.testops_ids,
        [suite.title for suite in relation.suite.data] + [scenario.name],
        result.params
    )

    return result


def __parse_parameters(scenario):
    row = scenario._row

    return {name: value for name, value in zip(row.headings, row.cells)} if row else {}


def __parse_tags(tags, logger=None) -> dict:
    meta_data = {}

    for tag in tags:
        # A typo in one tag must not abort the behave run.
        try:
            __parse_tag(tag, meta_data)
        except (ValueError, IndexError) as e:
            if logger:
                logger.log(f"Ignoring malformed tag @{tag}: {e}", "warning")

    return meta_data


VALUE_TAGS = ("qase.id", "qase.fields", "qase.tags", "qase.suite")


def __parse_tag(tag: str, meta_data: dict) -> None:
    tag_lower = tag.lower()

    if tag_lower.startswith("qase.project_id."):
        # Format: @qase.project_id.PROJ1:123,124
        project_part, ids_str = tag.split(":", 1)
        project_code = project_part.split(".", 2)[2]
        if not project_code:
            raise ValueError("expected @qase.project_id.CODE:1,2")
        meta_data.setdefault(TESTOPS_PROJECT_ID, {})[project_code] = __parse_ids(ids_str)
    elif tag_lower.startswith("qase.id:"):
        meta_data[TESTOPS_ID] = __parse_ids(tag.split(":", 1)[1])
    elif tag_lower.startswith("qase.fields:"):
        meta_data[FIELDS] = __extract_fields(tag)
    elif tag_lower.startswith("qase.tags:"):
        tag_values = tag.split(":", 1)[1].split(",")
        meta_data.setdefault(TAGS, []).extend(t.strip() for t in tag_values if t.strip())
    elif tag_lower.startswith("qase.suite:"):
        meta_data[SUITE] = tag.split(":", 1)[1].split('||')
    elif tag_lower == "qase.ignore":
        meta_data[IGNORE] = True
    elif tag_lower in VALUE_TAGS or tag_lower.startswith(tuple(f"{name}." for name in VALUE_TAGS)):
        raise ValueError(f"expected @{tag_lower.split('.')[0]}.{tag_lower.split('.')[1]}:<value>")


def __parse_ids(value: str) -> List[int]:
    ids = [int(x) for x in (part.strip() for part in value.split(',')) if x]
    if not ids:
        raise ValueError("no case IDs")
    return ids


def __extract_fields(tag: str) -> dict:
    value = tag.split(':', 1)[-1].strip()
    try:
        fields = json.loads(value)
        for key, value in fields.items():
            fields[key] = str(value).replace("_", " ")

        return fields
    except ValueError:
        return {}


def parse_scenario_from_json(
    scenario_dict: dict,
    feature_filename: str,
    time_offset: float = 0.0,
    logger=None,
) -> Result:
    """Parse a BehaveX JSON scenario dict into a Qase Result.

    ``time_offset`` (seconds) is added to every absolute timestamp read
    from BehaveX so the original timeline can be replayed inside the
    current Qase run window. See ``QaseFormatter._compute_time_offset``.
    """
    tags = __parse_tags(scenario_dict.get('tags', []), logger)

    name = scenario_dict.get('name', '')
    result = Result(name, name)

    project_ids = tags.get(TESTOPS_PROJECT_ID, None)
    if project_ids:
        for project_code, testops_ids in project_ids.items():
            result.set_testops_project_mapping(project_code, testops_ids)
    else:
        result.testops_ids = tags.get(TESTOPS_ID, None)

    result.fields = tags.get(FIELDS, {})
    result.ignore = tags.get(IGNORE, False)

    tag_list = tags.get(TAGS, [])
    if tag_list:
        result.add_tags(tag_list)

    relation = Relation()
    if SUITE in tags:
        for suite in tags[SUITE]:
            relation.suite.add_data(SuiteData(suite))
    else:
        suites = feature_filename.split(os.sep)
        for suite in suites:
            relation.suite.add_data(SuiteData(suite))
    result.relations = relation

    result.params = scenario_dict.get('parameters', {})

    status_map = {
        'passed': 'passed',
        'failed': 'failed',
        'error': 'invalid',
        'skipped': 'skipped',
        'undefined': 'invalid',
        'untested': 'skipped',
    }
    result.execution.set_status(
        status_map.get(scenario_dict.get('status', 'skipped'), 'skipped')
    )

    duration = scenario_dict.get('duration', 0)
    result.execution.duration = int(duration * 1000)
    start_ms = scenario_dict.get('start')
    stop_ms = scenario_dict.get('stop')
    if start_ms is not None and stop_ms is not None:
        result.execution.start_time = (start_ms / 1000.0) + time_offset
        result.execution.end_time = (stop_ms / 1000.0) + time_offset
    else:
        # Fallback when BehaveX did not record absolute timestamps:
        # synthesise a window ending "now" with the recorded duration.
        current_time = QaseUtils.get_real_time()
        result.execution.end_time = current_time
        result.execution.start_time = current_time - duration

    worker_id = scenario_dict.get('worker_id')
    if worker_id is not None:
        result.execution.thread = f"worker-{worker_id}"

    error_msg = scenario_dict.get('error_msg')
    if error_msg:
        if isinstance(error_msg, list):
            result.execution.stacktrace = '\n'.join(error_msg)
        else:
            result.execution.stacktrace = str(error_msg)

    result.signature = QaseUtils.get_signature(
        result.testops_ids,
        [suite.title for suite in relation.suite.data] + [name],
        result.params
    )

    return result


def parse_step_from_json(step_dict: dict, time_offset: float = 0.0) -> QaseStep:
    """Parse a BehaveX JSON step dict into a Qase Step.

    See ``parse_scenario_from_json`` for the ``time_offset`` contract.
    """
    keyword = step_dict.get('step_type', 'given')
    name = step_dict.get('name', '')
    line = step_dict.get('line', 0)

    model = QaseStep(
        step_type=StepType.GHERKIN,
        id=str(uuid.uuid4()),
        data=StepGherkinData(keyword=keyword, name=name, line=line)
    )

    status_mapping = {
        'passed': 'passed',
        'failed': 'failed',
        'error': 'failed',
        'skipped': 'skipped',
        'undefined': 'failed',
        'untested': 'skipped',
    }
    model.execution.set_status(
        status_mapping.get(step_dict.get('status', 'skipped'), 'skipped')
    )

    duration = step_dict.get('duration', 0)
    model.execution.duration = int(duration * 1000)
    start_ms = step_dict.get('start')
    stop_ms = step_dict.get('stop')
    if start_ms is not None and stop_ms is not None:
        model.execution.start_time = (start_ms / 1000.0) + time_offset
        model.execution.end_time = (stop_ms / 1000.0) + time_offset
    else:
        current_time = QaseUtils.get_real_time()
        model.execution.end_time = current_time
        model.execution.start_time = current_time - duration

    return model


def parse_step(step: Step, start_time: float = None) -> QaseStep:
    """Build a Qase Step model from a behave step result.

    ``start_time`` is the wall-clock instant captured by
    ``QaseFormatter.step()`` just before behave handed control to the
    step body — it excludes ``after_step`` hook latency that would
    otherwise contaminate every subsequent step's start_time.

    If no ``start_time`` is supplied (legacy callers, BehaveX JSON
    replay) fall back to ``now - step.duration``.
    """
    model = QaseStep(
        step_type=StepType.GHERKIN,
        id=str(uuid.uuid4()),
        data=StepGherkinData(keyword=step.keyword, name=step.name, line=step.line)
    )

    # Map behave status to qase status. The failed-vs-invalid decision is
    # made in the formatter, from ``step.hook_failed`` (present since behave
    # 1.2.6) rather than from any of these names, so 'error'/'hook_error'/
    # 'cleanup_error' (behave >=1.3's richer Status enum; absent on 1.2.6)
    # only need to route into the same "failed" branch here.
    status_mapping = {
        'passed': 'passed',
        'failed': 'failed',
        'error': 'failed',
        'hook_error': 'failed',
        'cleanup_error': 'failed',
        'skipped': 'skipped',
        'undefined': 'failed',
        'pending': 'skipped'
    }
    model.execution.set_status(status_mapping.get(step.status.name, 'skipped'))
    model.execution.duration = int(step.duration * 1000)

    if start_time is not None:
        # Anchor to the real moment behave called formatter.step(); use
        # behave's recorded duration for end_time so any after_step hook
        # latency in the result() callback doesn't inflate end_time.
        model.execution.start_time = start_time
        model.execution.end_time = start_time + step.duration
    else:
        current_time = QaseUtils.get_real_time()
        model.execution.end_time = current_time
        model.execution.start_time = current_time - step.duration

    return model
