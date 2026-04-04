#!/usr/bin/env python3
"""Clean up expected YAML files by removing dynamic and empty fields."""

import sys

import yaml
from pathlib import Path


def clean_result(result: dict) -> dict:
    """Remove dynamic, empty, and default fields from a result."""
    out = {}

    if result.get("title"):
        out["title"] = result["title"]
    if result.get("signature"):
        out["signature"] = result["signature"]
    if result.get("testops_ids"):
        out["testops_ids"] = result["testops_ids"]

    # Status (top-level shorthand from execution block)
    status = result.get("status") or (result.get("execution", {}) or {}).get("status")
    if status:
        out["status"] = status

    # Non-empty fields (remove None values like suite: null)
    fields = result.get("fields")
    if fields and fields != {}:
        cleaned_fields = {k: v for k, v in fields.items() if v is not None}
        if cleaned_fields:
            out["fields"] = cleaned_fields

    # Params (non-empty)
    params = result.get("params")
    if params and params != {}:
        out["params"] = params

    # Param groups (non-empty)
    param_groups = result.get("param_groups")
    if param_groups and param_groups != []:
        out["param_groups"] = param_groups

    # Relations (suites) — strip public_id from suite data
    relations = result.get("relations")
    if relations and relations.get("suite", {}).get("data"):
        clean_suite_data = []
        for item in relations["suite"]["data"]:
            clean_item = {k: v for k, v in item.items() if k != "public_id"}
            clean_suite_data.append(clean_item)
        out["relations"] = {"suite": {"data": clean_suite_data}}

    # Steps — clean recursively
    steps = result.get("steps")
    if steps and steps != []:
        out["steps"] = [clean_step(s) for s in steps]

    # Attachments — keep only file_name and mime_type
    attachments = result.get("attachments")
    if attachments and attachments != []:
        out["attachments"] = [clean_attachment(a) for a in attachments]

    # Muted only if true
    if result.get("muted"):
        out["muted"] = True

    # Skip: message (dynamic timestamps, unstable whitespace)
    # Skip: stacktrace (absolute file paths)
    # Skip: execution block (dynamic start_time, end_time, duration)

    return out


def clean_step(step: dict) -> dict:
    """Clean a step, removing IDs and timestamps."""
    out = {}

    data = step.get("data")
    if data:
        clean_data = {}
        if data.get("action"):
            clean_data["action"] = data["action"]
        if data.get("expected_result"):
            clean_data["expected_result"] = data["expected_result"]
        if clean_data:
            out["data"] = clean_data

    # Keep execution status and attachments (cleaned)
    exec_block = step.get("execution", {}) or {}
    if exec_block.get("status"):
        clean_exec = {"status": exec_block["status"]}
        exec_attachments = exec_block.get("attachments")
        if exec_attachments and exec_attachments != []:
            clean_exec["attachments"] = [clean_attachment(a) for a in exec_attachments]
        out["execution"] = clean_exec

    # Recursive child steps
    child_steps = step.get("steps")
    if child_steps and child_steps != []:
        out["steps"] = [clean_step(s) for s in child_steps]

    # Step-level attachments (if present)
    attachments = step.get("attachments")
    if attachments and attachments != []:
        out["attachments"] = [clean_attachment(a) for a in attachments]

    return out


def clean_attachment(att: dict) -> dict:
    """Keep only file_name and mime_type."""
    out = {}
    if att.get("file_name"):
        out["file_name"] = att["file_name"]
    if att.get("mime_type"):
        out["mime_type"] = att["mime_type"]
    return out


def clean_expected(data: dict) -> dict:
    """Clean an entire expected file."""
    out = {}

    if data.get("run"):
        out["run"] = data["run"]

    if data.get("results"):
        out["results"] = [clean_result(r) for r in data["results"]]

    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: clean_expected.py <file.yaml> [file2.yaml ...]")
        sys.exit(1)

    for path_str in sys.argv[1:]:
        path = Path(path_str)
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        cleaned = clean_expected(data)

        with open(path, "w") as f:
            yaml.dump(
                cleaned, f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        print(f"Cleaned: {path}")


if __name__ == "__main__":
    main()
