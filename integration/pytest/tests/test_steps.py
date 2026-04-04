"""Tests demonstrating step tracking: decorator, context manager, nested."""
from qase.pytest import qase


@qase.step("Step one")
def step_one():
    return True


@qase.step("Step two")
def step_two():
    return True


@qase.id(501)
@qase.title("Test with step decorators")
def test_step_decorators():
    result1 = step_one()
    assert result1
    result2 = step_two()
    assert result2


@qase.id(502)
@qase.title("Test with context manager steps")
def test_context_manager_steps():
    with qase.step("First inline step"):
        x = 1 + 1
        assert x == 2

    with qase.step("Second inline step"):
        y = 2 * 3
        assert y == 6


@qase.step("Parent step")
def parent_step():
    @qase.step("Child step A")
    def child_a():
        return True

    @qase.step("Child step B")
    def child_b():
        return True

    child_a()
    child_b()


@qase.id(503)
@qase.title("Test with nested steps")
def test_nested_steps():
    parent_step()
    assert True


@qase.id(504)
@qase.title("Test with failing step")
def test_failing_step():
    with qase.step("Passing step"):
        assert True

    with qase.step("Failing step"):
        assert False, "Step failure"
