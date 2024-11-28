import json
import os
import uuid
from typing import List

from behave.model import Scenario, Step
from qase.commons.models import Result, Relation
from qase.commons.models.relation import SuiteData
from qase.commons.models.step import StepType, StepGherkinData, Step as QaseStep

SUITE = "suite"
IGNORE = "ignore"
FIELDS = "fields"
TESTOPS_ID = "testops_id"


def filter_scenarios(case_ids: List[int], scenarios: List[Scenario]) -> List[Scenario]:
    if not case_ids:
        return scenarios

    executed_scenarios = []
    for scenario in scenarios:
        tags = __parse_tags(scenario.tags)
        if TESTOPS_ID in tags:
            if int(tags[TESTOPS_ID]) in case_ids:
                executed_scenarios.append(scenario)

    return executed_scenarios


def parse_scenario(scenario: Scenario) -> Result:
    tags = __parse_tags(scenario.tags)

    result = Result(scenario.name, scenario.name)

    result.testops_id = tags.get(TESTOPS_ID, None)
    result.fields = tags.get(FIELDS, {})
    result.ignore = tags.get(IGNORE, False)

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

    return result


def __parse_parameters(scenario):
    row = scenario._row

    return {name: value for name, value in zip(row.headings, row.cells)} if row else {}


def __parse_tags(tags) -> dict:
    meta_data = {}

    for tag in tags:
        if tag.lower().startswith("qase.id"):
            meta_data[TESTOPS_ID] = int(tag.split(":")[1])
            continue

        if tag.lower().startswith("qase.fields"):
            meta_data[FIELDS] = __extract_fields(tag)
            continue

        if tag.lower() == "qase.ignore":
            meta_data[IGNORE] = True

        if tag.lower().startswith("qase.suite"):
            meta_data[SUITE] = tag.split(":")[1].split('||')

    return meta_data


def __extract_fields(tag: str) -> dict:
    value = tag.split(':', 1)[-1].strip()
    try:
        fields = json.loads(value)
        for key, value in fields.items():
            fields[key] = str(value).replace("_", " ")

        return fields
    except ValueError:
        return {}


def parse_step(step: Step) -> QaseStep:
    model = QaseStep(
        step_type=StepType.GHERKIN,
        id=str(uuid.uuid4()),
        data=StepGherkinData(keyword=step.keyword, name=step.name, line=step.line)
    )

    model.execution.set_status(step.status.name)

    return model
