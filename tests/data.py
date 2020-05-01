def _project():
    return {
        "title": "Demo Project",
        "code": "DEMO",
        "counts": {
            "cases": 10,
            "suites": 3,
            "milestones": 0,
            "runs": {"total": 1, "active": 1},
            "defects": {"total": 0, "open": 0},
        },
    }


def _test_case():
    return {
        "id": 5,
        "position": 1,
        "title": "Test case",
        "description": "Description for case",
        "preconditions": "",
        "postconditions": "",
        "severity": 4,
        "priority": 2,
        "type": 1,
        "behavior": 2,
        "automation": "is-not-automated",
        "status": "actual",
        "milestone_id": None,
        "suite_id": 1,
        "tags": [],
        "links": [],
        "revision": 1,
        "custom_fields": [],
        "attachments": [],
        "steps": [],
        "created": "2018-05-02T20:32:23.000000Z",
        "updated": "2019-07-21T13:24:08.000000Z",
    }


def _list(data):
    return {"total": 10, "filtered": 10, "count": 1, "entities": [data]}


def _status_true(data):
    return {"status": True, "result": data}
