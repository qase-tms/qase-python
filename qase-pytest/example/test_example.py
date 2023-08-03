from qaseio.pytest import qase

import time


@qase.step("Capitalize step")
def capital_case(x):
    return x.capitalize()


@qase.id(1)
@qase.title('Test should pass')
@qase.fields(
    ("severity", "critical"),
    ("priority", "hight"),
    ("layer", "unit"),
    ("description", "Always passes"),
    ("description", "*Precondition 1*. None."),
)
def test_capital_case():
    with qase.step("First step"):
        time.sleep(0)
    assert capital_case('semaphor') == 'Semaphor'


@qase.id(2)
@qase.title("Test should fail")
@qase.fields(
    ("severity", "critical"),
    ("priority", "hight"),
    ("layer", "unit"),
    ("description", "Always fails"),
    ("description", "*Precondition 1*. None."),
)
def test_capital_case2():
    with qase.step("Failed step"):
        assert capital_case('semaphor') == 'semaphor'