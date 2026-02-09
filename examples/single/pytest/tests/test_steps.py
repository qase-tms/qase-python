from qase.pytest import qase


@qase.step("Step 01")
def step01():
    step02()
    pass


@qase.step("Step 02")
def step02():
    pass


def test_with_steps_success():
    step01()
    with qase.step("Step 03"):
        pass
    assert 1 == 1


def test_with_steps_failed():
    step01()
    with qase.step("Step 03"):
        pass
    assert 1 == 2
