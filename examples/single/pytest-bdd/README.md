# qase-pytest + pytest-bdd example

A runnable demo of the native pytest-bdd integration in qase-pytest.
Exercises every feature of the integration so you can see how each kind
of Gherkin construct is reported in Qase.

## What the example covers

| Feature file | Scenario(s) | Demonstrates |
| --- | --- | --- |
| `login.feature` | Successful login | Basic Given/When/Then with nested `qase.step()` calls — sub-steps appear as children of the Gherkin step. |
| `failing.feature` | A failing assertion in the middle step | A failing Then step. The failed step is marked `failed`; pytest-bdd does not run later steps, but the integration records them as `skipped`. |
| `calculator.feature` | Scenario Outline with 3 example rows | Scenario Outline / Examples — produces three parameterized Qase results for the same scenario. |
| `data_carriers.feature` | Step with a data table and a docstring | DataTable rendered as a markdown table, DocString rendered as a fenced code block — both end up in the step `data` payload. |
| `checkout.feature` | Two scenarios sharing a Background | Background steps run before each scenario and are reported on every scenario's result. Multi-scenario feature with distinct `@qase.id=`, `@qase.suite=` tags per scenario. |

## Recognized scenario tags

Tags must be placed on the `Scenario` line (not the `Feature` line) so
they reach `scenario.tags`:

- `@qase.id=NN` — link to a test case
- `@qase.suite=A.B.C` — override suite chain (dot for nesting)
- `@qase.severity=critical` / `@qase.priority=high` / `@qase.layer=e2e`
- `@qase.ignore` — drop the scenario from the report
- `@qase.muted` — don't let the scenario fail the run

## Run locally (report mode)

```bash
pip install -r requirements.txt
pytest -v
```

5 scenarios execute (one failing on purpose). Inspect the produced JSON
under `build/qase-report/results/`:

- Each result has the scenario name as `title`
- Each result has a suite chain matching the `@qase.suite` tag
- Each result has a list of `steps` mirroring the Gherkin steps in order
- Nested `qase.step(...)` calls (inside step functions) appear as
  children of the corresponding Gherkin step
- Failed step has `execution.status: "failed"`; trailing unrun steps
  are marked `"skipped"`
- Scenario Outline produces one Qase result per Examples row

## Run against Qase TestOps

Set `mode` to `testops` in `qase.config.json`, and provide credentials
via env:

```bash
export QASE_TESTOPS_API_TOKEN=...
export QASE_TESTOPS_PROJECT=PROJ_CODE
pytest -v
```

The TestOps API mode preserves native Gherkin step structure (keyword
+ name + data) and renders steps with their Given/When/Then keywords
in the Qase UI.
