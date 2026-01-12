#!/usr/bin/env python3
"""
Pre-commit hook to check that pytest test functions have qase.id() decorator.

This hook scans staged Python files that look like pytest test modules
and detects test functions/methods that do NOT have a qase.id() decorator.
"""

import argparse
import ast
import sys
from pathlib import Path
from typing import List, Tuple, Optional


class QaseIdChecker(ast.NodeVisitor):
    """AST visitor to find test functions without qase.id() decorator."""

    def __init__(self, filename: str):
        self.filename = filename
        self.issues: List[Tuple[int, str]] = []
        self.current_class: Optional[str] = None

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definitions to track test classes."""
        # Check if it's a test class (starts with Test)
        old_class = self.current_class
        if node.name.startswith("Test"):
            self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definitions to check for qase.id() decorator."""
        # Check if it's a test function (starts with test_)
        is_test_function = node.name.startswith("test_")
        
        # Check if it's a test method in a test class
        is_test_method = (
            self.current_class is not None
            and node.name.startswith("test_")
        )

        if is_test_function or is_test_method:
            # Check for qase.id() or qase.ignore() decorator
            has_qase_id = False
            has_qase_ignore = False

            for decorator in node.decorator_list:
                if self._is_qase_id_decorator(decorator):
                    has_qase_id = True
                    break
                if self._is_qase_ignore_decorator(decorator):
                    has_qase_ignore = True
                    break

            # If neither qase.id() nor qase.ignore() is present, it's an issue
            if not has_qase_id and not has_qase_ignore:
                test_name = node.name
                if self.current_class:
                    test_name = f"{self.current_class}.{test_name}"
                self.issues.append((node.lineno, test_name))

        self.generic_visit(node)

    def _is_qase_id_decorator(self, decorator: ast.expr) -> bool:
        """Check if decorator is @qase.id(...)."""
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Attribute):
                if (
                    isinstance(decorator.func.value, ast.Name)
                    and decorator.func.value.id == "qase"
                    and decorator.func.attr == "id"
                ):
                    return True
        return False

    def _is_qase_ignore_decorator(self, decorator: ast.expr) -> bool:
        """Check if decorator is @qase.ignore()."""
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Attribute):
                if (
                    isinstance(decorator.func.value, ast.Name)
                    and decorator.func.value.id == "qase"
                    and decorator.func.attr == "ignore"
                ):
                    return True
        return False


def is_pytest_test_file(filepath: Path) -> bool:
    """Check if file looks like a pytest test module."""
    name = filepath.name
    # Check common pytest test file patterns
    return (
        name.startswith("test_")
        or name.endswith("_test.py")
        or (name.startswith("test") and name.endswith(".py"))
    )


def check_file(filepath: Path) -> List[Tuple[int, str]]:
    """Check a single file for missing qase.id() decorators."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(filepath))
        checker = QaseIdChecker(str(filepath))
        checker.visit(tree)
        return checker.issues
    except SyntaxError as e:
        # Skip files with syntax errors (they'll be caught by other tools)
        return []
    except Exception as e:
        # For other errors, print warning but don't fail
        print(f"Warning: Could not parse {filepath}: {e}", file=sys.stderr)
        return []


def main():
    """Main entry point for the hook."""
    parser = argparse.ArgumentParser(
        description="Check pytest tests for qase.id() decorator"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Python files to check",
    )
    parser.add_argument(
        "--warn",
        action="store_true",
        help="Warn only, don't fail the commit. By default, missing qase.id() blocks the commit.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Patterns to exclude (can be specified multiple times)",
    )

    args = parser.parse_args()

    # Default behavior: block commit. Only warn if --warn is explicitly set.
    warn_only = args.warn

    all_issues: List[Tuple[Path, int, str]] = []

    # If no files provided, exit successfully (pre-commit will handle filtering)
    if not args.files:
        return 0

    for file_arg in args.files:
        filepath = Path(file_arg)
        
        # Check if file should be excluded
        if any(pattern in str(filepath) for pattern in args.exclude):
            continue

        # Only check Python files that look like pytest tests
        if not filepath.suffix == ".py":
            continue

        if not is_pytest_test_file(filepath):
            continue

        if not filepath.exists():
            continue

        issues = check_file(filepath)
        for lineno, test_name in issues:
            all_issues.append((filepath, lineno, test_name))

    # Print results - always show messages
    if all_issues:
        # Use stdout for warn mode (pre-commit shows stdout even for successful hooks)
        # Use stderr for required mode (standard for errors)
        output_stream = sys.stdout if warn_only else sys.stderr
        
        print("Tests without qase.id() decorator found:", file=output_stream)
        for filepath, lineno, test_name in all_issues:
            print(f"  {filepath}:{lineno}  → {test_name}", file=output_stream)
        
        if warn_only:
            print("\n(Warning only - commit will proceed)", file=output_stream)
            # Flush to ensure output is visible
            output_stream.flush()
            return 0
        else:
            print("\nPlease add @qase.id(...) or @qase.ignore() to these tests.", file=output_stream)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
