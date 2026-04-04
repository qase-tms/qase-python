"""Tests demonstrating field metadata: severity, priority, layer, description, preconditions, postconditions."""
from qase.pytest import qase


@qase.id(201)
@qase.title("Test with severity blocker")
@qase.severity("blocker")
def test_severity_blocker():
    assert True


@qase.id(202)
@qase.title("Test with priority high")
@qase.priority("high")
def test_priority_high():
    assert True


@qase.id(203)
@qase.title("Test with layer e2e")
@qase.layer("e2e")
def test_layer_e2e():
    assert True


@qase.id(204)
@qase.title("Test with description")
@qase.description("This test verifies that description field is reported correctly.")
def test_description():
    assert True


@qase.id(205)
@qase.title("Test with preconditions and postconditions")
@qase.preconditions("User is logged in")
@qase.postconditions("Session is active")
def test_conditions():
    assert True


@qase.id(206)
@qase.title("Test with multiple fields via @qase.fields")
@qase.fields(
    ("severity", "critical"),
    ("priority", "high"),
    ("layer", "api"),
)
def test_multiple_fields():
    assert True


@qase.id(207)
@qase.title("Test with author")
@qase.author("integration-bot")
def test_author():
    assert True


@qase.id(208)
@qase.title("Muted test")
@qase.muted()
def test_muted():
    assert True
