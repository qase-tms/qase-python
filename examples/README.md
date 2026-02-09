# Qase Python Examples

This directory contains working examples for all Qase Python reporters.

## Directory Structure

| Directory | Mode | Description |
|-----------|------|-------------|
| [single/](./single/) | `testops` | Report results to a single Qase project |
| [multiproject/](./multiproject/) | `testops_multi` | Report results to multiple Qase projects |

## Quick Start

1. Choose your framework and mode
2. Navigate to the example directory
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `qase.config.json` with your API token and project code
5. Run the tests

## Single Project Examples

Report all test results to one Qase project using `mode: testops`.

```
single/
├── pytest/          # Pytest examples (basic, attachments, steps, profilers)
├── behave/          # Behave BDD examples
├── robot/           # Robot Framework examples
└── tavern/          # Tavern API testing examples
```

See [single/README.md](./single/README.md) for details.

## Multi-Project Examples

Report test results to multiple Qase projects simultaneously using `mode: testops_multi`.

```
multiproject/
├── pytest/          # @qase.project_id() decorator
├── behave/          # @qase.project_id.CODE:ID tags
├── robot/           # Q-PROJECT.CODE-ID tags
└── tavern/          # QaseProjectID.CODE=ID in test names
```

See [multiproject/README.md](./multiproject/README.md) for details.

## Configuration

All examples use `qase.config.json` for configuration. Before running:

1. Copy the example config or edit existing one
2. Replace `<token>` with your [Qase API token](https://app.qase.io/user/api/token)
3. Replace `<project_code>` with your project code (from URL: `app.qase.io/project/CODE`)

For complete configuration reference, see [qase-python-commons](../qase-python-commons/README.md).

## Framework Documentation

| Framework | Package | Documentation |
|-----------|---------|---------------|
| Pytest | `qase-pytest` | [README](../qase-pytest/README.md) \| [Usage Guide](../qase-pytest/docs/usage.md) |
| Behave | `qase-behave` | [README](../qase-behave/README.md) \| [Usage Guide](../qase-behave/docs/usage.md) |
| Robot Framework | `qase-robotframework` | [README](../qase-robotframework/README.md) \| [Usage Guide](../qase-robotframework/docs/usage.md) |
| Tavern | `qase-tavern` | [README](../qase-tavern/README.md) \| [Usage Guide](../qase-tavern/docs/usage.md) |
