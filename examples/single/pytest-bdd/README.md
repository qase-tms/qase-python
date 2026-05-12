# qase-pytest + pytest-bdd example

Reproduces the customer feedback scenario: a single Gherkin login
scenario with three steps, each containing a nested manual step via
`qase.step(...)`.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

Inspect the produced JSON under `build/qase-report/results/` — the
result has the scenario name as title, the feature/suite hierarchy from
the tag, three top-level Gherkin steps, and one sub-step under each.

To send to Qase TestOps instead, set `mode` to `testops` in
`qase.config.json` and provide `QASE_TESTOPS_API_TOKEN` and
`QASE_TESTOPS_PROJECT` via env.
