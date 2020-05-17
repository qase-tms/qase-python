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


def _test_run():
    return {
        "id": 1,
        "title": "Test run 2019/12/12",
        "description": None,
        "status": 0,
        "start_time": "2019-12-12 12:12:12",
        "end_time": None,
        "public": False,
        "stats": {
            "total": 3,
            "untested": 3,
            "passed": 0,
            "failed": 0,
            "blocked": 0,
            "skipped": 0,
            "retest": 0,
            "deleted": 4,
        },
        "time_spent": 0,
        "user_id": 1,
        "environment": None,
        "cases": [1, 2, 3],
    }


def _test_plan():
    return {
        "id": 1,
        "title": "Sample plan",
        "description": "Regression",
        "cases_count": 10,
        "created": "2019-01-10T22:47:53.000000Z",
        "updated": "2019-01-10T22:47:53.000000Z",
    }


def _test_plan_full():
    return {
        "id": 16,
        "title": "Sample plan",
        "description": "Awesome plan",
        "cases_count": 1,
        "created": "2019-09-15T18:49:07.000000Z",
        "updated": "2019-09-15T18:49:30.000000Z",
        "average_time": 40,
        "cases": [{"case_id": 1, "assignee_id": 1}],
    }


def _test_suite():
    return {
        "id": 1,
        "title": "Level 1",
        "description": "Set from API",
        "preconditions": "Set from API",
        "position": 1,
        "cases_count": 10,
        "parent_id": None,
        "created": "2018-05-02T10:49:01.000000Z",
        "updated": "2019-07-21T19:10:15.000000Z",
    }


def _shared_step():
    return {
        "hash": "0223905c291bada23e6049d415385982af92d758",
        "title": "Shared step",
        "action": "Open signup page",
        "expected_result": "Page is opened",
        "cases": [41, 35, 42, 30],
        "cases_count": 4,
        "created": "2019-02-09T23:16:49.000000Z",
        "updated": "2019-02-09T23:16:49.000000Z",
    }


def _test_run_result():
    return {
        "hash": "6efce6e4f9de887a2ee863e8197cb74ab626a273",
        "comment": "some comment",
        "stacktrace": "some stacktrace",
        "run_id": 1,
        "case_id": 1,
        "steps": None,
        "status": "Passed",
        "is_api_result": True,
        "time_spent": 0,
        "end_time": "2018-11-11 11:11:11",
        "attachments": [
            "6efce6e4f9de887a2ee863e8197cb74ab626a271",
            "6efce6e4f9de887a2ee863e8197cb74ab626a272",
        ],
    }


def _defect():
    return {
        "id": 1,
        "title": "Dangerous defect",
        "actual_result": "Something happened",
        "status": "open",
        "user_id": 1,
        "attachments": [],
        "created": "2019-11-08T22:03:07.000000Z",
        "updated": "2019-11-19T22:29:57.000000Z",
    }


def _attachment():
    return {
        "hash": "2497be4bc95f807d2fe3c2203793673f6e5140e8",
        "file": "filename.ext",
        "mime": "text/plain",
        "size": 100,
        "full_path": "https://storage.cdn.example/filename.ext",
    }


def _attachment_created():
    return {
        "filename": "qaseio_pytest.py",
        "url": "https://storage.cdn.example/filename.ext",
        "extension": "py",
        "hash": "d81bb2beb147c2eceddbf3e10f98e6216cc757e3",
        "mime": "text\\/x-python",
        "team": "c66dc393c83fe149449e5de3e64545279e1442ed",
    }


def _custom_field():
    return {
        "id": 1,
        "title": "Description",
        "type": "Text",
        "placeholder": "Write something",
        "default_value": None,
        "value": None,
        "is_required": False,
        "is_visible": False,
        "is_filterable": False,
        "created": "2019-08-26T22:30:07.000000Z",
        "updated": "2019-08-26T22:30:07.000000Z",
    }


def _user():
    return {
        "id": 1,
        "name": "John Smith",
        "email": "john@example.com",
        "title": "Team Owner",
        "status": 1,
    }


def _list(data):
    return {"total": 10, "filtered": 10, "count": 1, "entities": [data]}


def _status_true(data):
    return {"status": True, "result": data}
