from robot.api.deco import keyword


@keyword("Step 01")
def step01():
    pass


@keyword("Step 02")
def step02():
    pass


@keyword("Passed step")
def passed_step():
    pass


@keyword("Failed step")
def failed_step():
    assert False
