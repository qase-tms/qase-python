"""Native pytest-bdd integration for qase-pytest.

Loaded conditionally from conftest.py only when pytest_bdd is installed.
"""

import ast as _ast
import re
import warnings as _warnings
from typing import Iterable, Optional

from qase.commons.models.relation import Relation, SuiteData
from qase.commons.models.step import Step, StepGherkinData, StepType


class QasePytestBddPlugin:
    """Bridge between pytest-bdd hooks and the main QasePytestPlugin runtime."""

    def __init__(self, pytest_plugin):
        self._pytest_plugin = pytest_plugin
        self._current = None  # per-scenario state dict
        self._install_warning_filter()

    @staticmethod
    def _install_warning_filter():
        """Silence pytest-bdd-forwarded Gherkin tags showing up as unknown marks.

        pytest-bdd 7+/8 turns every Gherkin scenario tag into a pytest marker
        whose name is the raw tag string (e.g. ``qase.id=42``). pytest emits
        ``PytestUnknownMarkWarning`` for each unique one. The warnings have
        no diagnostic value for the user (it's not a typo — the tag is
        intentional), so we silence ONLY the qase.* family. Other unknown
        marks still warn normally.
        """
        try:
            # local import — pytest is always installed when this plugin loads
            import pytest as _pytest

            category = getattr(_pytest, "PytestUnknownMarkWarning", Warning)
        except Exception:
            category = Warning

        _warnings.filterwarnings(
            "ignore",
            message=r"Unknown pytest\.mark\.qase\.",
            category=category,
        )

    def pytest_bdd_before_scenario(self, request, feature, scenario):
        runtime = getattr(self._pytest_plugin, "runtime", None)
        if runtime is None or runtime.result is None:
            return

        enrich_result_from_scenario(runtime.result, feature, scenario)

        # Build the ordered cache: background steps first, then scenario steps,
        # de-duplicated by identity in case pytest-bdd already merges them.
        background = getattr(feature, "background", None) or getattr(
            scenario, "background", None
        )
        bg_steps = list(getattr(background, "steps", []) or []) if background else []
        sc_steps = list(getattr(scenario, "steps", []) or [])
        seen = set()
        remaining = []
        for s in bg_steps + sc_steps:
            sid = id(s)
            if sid in seen:
                continue
            seen.add(sid)
            remaining.append(s)

        self._current = {
            "remaining_steps": remaining,
            "next_step_idx": 0,
            "bdd_step_to_id": {},  # id(bdd_step) -> qase Step.id
            "scenario_failed": False,
        }

    def pytest_bdd_before_step(self, request, feature, scenario, step, step_func):
        runtime = getattr(self._pytest_plugin, "runtime", None)
        if runtime is None or self._current is None:
            return
        qase_step = build_step(step)
        runtime.add_step(qase_step)
        self._current["bdd_step_to_id"][id(step)] = qase_step.id
        self._current["next_step_idx"] += 1

    def pytest_bdd_after_step(
        self, request, feature, scenario, step, step_func, step_func_args
    ):
        runtime = getattr(self._pytest_plugin, "runtime", None)
        if runtime is None or self._current is None:
            return
        qase_step_id = self._current["bdd_step_to_id"].get(id(step))
        if qase_step_id is None:
            return
        runtime.finish_step(qase_step_id, status="passed")

    def pytest_bdd_step_error(
        self, request, feature, scenario, step, step_func, step_func_args, exception
    ):
        runtime = getattr(self._pytest_plugin, "runtime", None)
        if runtime is None or self._current is None:
            return
        qase_step_id = self._current["bdd_step_to_id"].get(id(step))
        if qase_step_id is not None:
            runtime.finish_step(qase_step_id, status="failed")
        self._current["scenario_failed"] = True

    def pytest_bdd_step_func_lookup_error(
        self, request, feature, scenario, step, exception
    ):
        runtime = getattr(self._pytest_plugin, "runtime", None)
        if runtime is None or self._current is None:
            return
        # No before_step fired — create the Step directly with status='invalid'.
        qase_step = build_step(step)
        qase_step.execution.set_status("invalid")
        qase_step.execution.complete()
        runtime.steps[qase_step.id] = qase_step
        self._current["scenario_failed"] = True

    def pytest_bdd_after_scenario(self, request, feature, scenario):
        runtime = getattr(self._pytest_plugin, "runtime", None)
        if runtime is None or self._current is None:
            return
        # Honor @qase.ignore: when set, drop the result so the reporter
        # doesn't emit it.
        if getattr(runtime.result, "ignore", False):
            runtime.result = None
            self._current = None
            return
        # Steps after the last reached one were skipped because of a prior failure.
        remaining = self._current["remaining_steps"][self._current["next_step_idx"] :]
        for s in remaining:
            qase_step = build_step(s)
            qase_step.execution.set_status("skipped")
            qase_step.execution.complete()
            runtime.steps[qase_step.id] = qase_step
        self._current = None


_KNOWN_FIELD_KEYS = {"severity", "priority", "layer", "description"}


def parse_scenario_tags(tags: Iterable[str]) -> dict:
    """Parse pytest-bdd scenario tags into Qase metadata.

    Recognized forms (single separator: '='):
        qase.id=123                       -> testops_ids
        qase.id=123,124                   -> testops_ids
        qase.project_id.CODE=1,2          -> testops_project_mapping
        qase.ignore                       -> ignore flag
        qase.muted                        -> muted flag
        qase.suite=A.B                    -> nested suites
        qase.severity= / priority= / layer= -> fields
    Any other tag (with or without '@' prefix) is appended to tags.
    """
    out = {
        "testops_ids": None,
        "testops_project_mapping": None,
        "ignore": False,
        "muted": False,
        "suite": None,
        "fields": {},
        "tags": [],
    }

    for raw in tags:
        tag = raw[1:] if raw.startswith("@") else raw
        lowered = tag.lower()

        if lowered == "qase.ignore":
            out["ignore"] = True
            continue
        if lowered == "qase.muted":
            out["muted"] = True
            continue

        if lowered.startswith("qase.id="):
            values = tag.split("=", 1)[1]
            ids = _parse_id_list(values)
            if ids:
                out["testops_ids"] = ids
            continue

        if lowered.startswith("qase.project_id."):
            # qase.project_id.CODE=1,2
            head, _, values = tag.partition("=")
            code = head.split(".", 2)[2] if head.count(".") >= 2 else None
            ids = _parse_id_list(values)
            if code and ids:
                if out["testops_project_mapping"] is None:
                    out["testops_project_mapping"] = {}
                out["testops_project_mapping"][code] = ids
            continue

        if lowered.startswith("qase.suite="):
            value = tag.split("=", 1)[1]
            out["suite"] = [s.strip() for s in value.split(".") if s.strip()]
            continue

        # qase.<known_field>=value
        if lowered.startswith("qase.") and "=" in lowered:
            key = lowered.split("=", 1)[0].split(".", 1)[1]
            if key in _KNOWN_FIELD_KEYS:
                out["fields"][key] = tag.split("=", 1)[1]
                continue

        # Unknown — treat as a free tag.
        out["tags"].append(tag)

    return out


def _parse_id_list(values: str) -> Optional[list]:
    parsed = []
    for chunk in re.split(r"\s*,\s*", values.strip()):
        if not chunk:
            continue
        try:
            parsed.append(int(chunk))
        except ValueError:
            return None
    return parsed or None


def format_data_table(table) -> str:
    """Render a pytest-bdd DataTable as a GitHub-flavored markdown table.

    Accepts a duck-typed object exposing `.rows[].cells[].value`. Returns "" if
    table is None or empty.
    """
    if table is None:
        return ""

    rows = getattr(table, "rows", None) or []
    if not rows:
        return ""

    def _row_values(row):
        return [_escape_markdown_table_cell(cell.value) for cell in row.cells]

    header_values = _row_values(rows[0])
    lines = [
        "| " + " | ".join(header_values) + " |",
        "| " + " | ".join(["---"] * len(header_values)) + " |",
    ]
    for row in rows[1:]:
        lines.append("| " + " | ".join(_row_values(row)) + " |")

    return "\n".join(lines)


def _escape_markdown_table_cell(value) -> str:
    """Escape characters that would break a markdown table row."""
    text = str(value)
    # Order matters: escape backslashes first so subsequently inserted
    # backslashes (from pipe escaping) are not re-doubled.
    text = text.replace("\\", "\\\\")
    text = text.replace("|", "\\|")
    # Newlines split table rows; map them to <br> which renders inside cells.
    text = text.replace("\r\n", "<br>").replace("\n", "<br>").replace("\r", "<br>")
    return text


def format_docstring(text) -> str:
    """Render a Gherkin step docstring as a fenced markdown code block.

    Returns "" for None/empty input. Outer leading/trailing newlines and
    trailing whitespace are stripped; internal indentation and internal
    trailing whitespace are preserved verbatim (Gherkin docstrings may
    contain semantically significant indentation, e.g. code samples).

    If the input contains a run of backticks, the wrapping fence is made
    one longer than the longest run found — preventing premature fence
    closure (standard CommonMark behavior).
    """
    if not text:
        return ""
    stripped = text.strip("\n").rstrip()
    if not stripped:
        return ""

    longest_run = 0
    for match in re.finditer(r"`+", stripped):
        longest_run = max(longest_run, len(match.group(0)))
    fence = "`" * max(3, longest_run + 1)

    return fence + "\n" + stripped + "\n" + fence


def build_step(bdd_step) -> Step:
    """Build a Qase Step(GHERKIN) from a pytest-bdd Step object.

    Reads keyword, name, line_number, data_table, docstring defensively so the
    helper survives minor API drifts between pytest-bdd versions. pytest-bdd
    >= 7 exposes the DataTable on ``datatable`` (no underscore); older or
    alternative API shapes may use ``data_table`` — accept either.
    """
    keyword = getattr(bdd_step, "keyword", "")
    name = getattr(bdd_step, "name", "")
    line = getattr(bdd_step, "line_number", 0) or 0

    data_table = getattr(bdd_step, "data_table", None) or getattr(
        bdd_step, "datatable", None
    )
    docstring = getattr(bdd_step, "docstring", None)

    payload = None
    table_md = format_data_table(data_table)
    if table_md:
        payload = table_md
    elif docstring:
        payload = format_docstring(docstring)

    return Step(
        step_type=StepType.GHERKIN,
        id=None,  # let Step generate uuid
        data=StepGherkinData(
            keyword=keyword,
            name=name,
            line=line,
            data=payload,
        ),
    )


def expand_pytest_bdd_example_params(result) -> None:
    """Explode pytest-bdd's `_pytest_bdd_example` param into individual keys.

    pytest-bdd 8.x converts a Scenario Outline row into a single parametrize
    argument `_pytest_bdd_example` whose value is a dict (sometimes already
    a dict, sometimes a repr string). We unpack it into one param per
    column for readable rendering in Qase, and drop the original key.

    No-op if the key is absent or its value cannot be parsed as a dict.
    """
    params = getattr(result, "params", None)
    if not params or "_pytest_bdd_example" not in params:
        return

    raw = params["_pytest_bdd_example"]
    parsed = raw
    if isinstance(parsed, str):
        try:
            parsed = _ast.literal_eval(parsed)
        except (ValueError, SyntaxError):
            return  # keep the original key — can't parse safely

    if not isinstance(parsed, dict):
        return

    # Remove the wrapper key only after we know the unpack will succeed.
    params.pop("_pytest_bdd_example", None)
    for key, value in parsed.items():
        params[str(key)] = str(value)


def enrich_result_from_scenario(result, feature, scenario) -> None:
    """Mutate an existing Result with metadata extracted from a pytest-bdd scenario."""
    if getattr(scenario, "name", None):
        result.title = scenario.name

    parsed = parse_scenario_tags(getattr(scenario, "tags", []) or [])

    feature_desc = (getattr(feature, "description", "") or "").strip()
    scenario_desc = (getattr(scenario, "description", "") or "").strip()
    description_parts = [p for p in (feature_desc, scenario_desc) if p]
    if description_parts:
        result.fields["description"] = "\n\n".join(description_parts)

    if parsed["suite"]:
        new_relation = Relation()
        for s in parsed["suite"]:
            new_relation.add_suite(SuiteData(title=s))
        result.relations = new_relation
    elif getattr(feature, "name", None):
        relation = result.relations or Relation()
        existing = list(getattr(relation.suite, "data", []) or [])
        new_relation = Relation()
        new_relation.add_suite(SuiteData(title=feature.name))
        for s in existing:
            new_relation.add_suite(s)
        result.relations = new_relation

    if parsed["testops_project_mapping"]:
        for code, ids in parsed["testops_project_mapping"].items():
            result.set_testops_project_mapping(code, ids)
    elif parsed["testops_ids"]:
        result.testops_ids = parsed["testops_ids"]

    for key, value in parsed["fields"].items():
        result.fields[key] = value

    if parsed["tags"]:
        result.add_tags(parsed["tags"])
    result.muted = parsed["muted"]
    result.ignore = parsed["ignore"]

    expand_pytest_bdd_example_params(result)
