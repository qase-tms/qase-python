"""Native pytest-bdd integration for qase-pytest.

Loaded conditionally from conftest.py only when pytest_bdd is installed.
"""

import re
from typing import Iterable, Optional


class QasePytestBddPlugin:
    """Bridge between pytest-bdd hooks and the main QasePytestPlugin runtime."""

    def __init__(self, pytest_plugin):
        self._pytest_plugin = pytest_plugin


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
