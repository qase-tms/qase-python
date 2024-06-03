from qase.pytest import qase


@qase.id(1)
def test_with_qase_id_success():
    assert 1 == 1


@qase.id(2)
def test_with_qase_id_failed():
    assert 1 == 2


@qase.title("Simple test success")
def test_with_title_success():
    assert 1 == 1


@qase.title("Simple test failed")
def test_with_title_failed():
    assert 1 == 2


@qase.description("Try to login to Qase TestOps using login and password 1")
def test_with_description_success():
    assert 1 == 1


@qase.description("Try to login to Qase TestOps using login and password")
def test_with_description_failed():
    assert 1 == 2


@qase.preconditions("*Precondition 1*. Markdown is supported.")
def test_with_preconditions_success():
    assert 1 == 1


@qase.preconditions("*Precondition 1*. Markdown is supported.")
def test_with_preconditions_failed():
    assert 1 == 2


@qase.postconditions("*Postcondition 1*. Markdown is supported.")
def test_with_postconditions_success():
    assert 1 == 1


@qase.postconditions("*Postcondition 1*. Markdown is supported.1")
def test_with_postconditions_failed():
    assert 1 == 2


@qase.severity("normal")
def test_with_severity_success():
    assert 1 == 1


@qase.severity("normal")
def test_with_severity_failed():
    assert 1 == 2


@qase.priority("high")
def test_with_priority_success():
    assert 1 == 1


@qase.priority("high")
def test_with_priority_failed():
    assert 1 == 2


@qase.layer("unit")
def test_with_layer_success():
    assert 1 == 1


@qase.layer("unit")
def test_with_layer_failed():
    assert 1 == 2


@qase.fields(
    ("severity", "normal"),
    ("custom_field", "value"),
    ("priority", "high"),
    ("layer", "unit"),
    ("description", "Try to login to Qase TestOps using login and password"),
    ("preconditions", "*Precondition 1*. Markdown is supported."),
    ("postconditions", "*Postcondition 1*. Markdown is supported."),
)
def test_with_fields_success():
    assert 1 == 1


@qase.fields(
    ("severity", "normal"),
    ("priority", "high"),
    ("layer", "unit"),
    ("description", "Try to login to Qase TestOps using login and password"),
    ("preconditions", "*Precondition 1*. Markdown is supported."),
    ("postconditions", "*Postcondition 1*. Markdown is supported."),
)
def test_with_fields_failed():
    assert 1 == 2
