from qaseio.pytest import qase


def capital_case(x):
    return x.capitalize()


@qase.id(1)
def test_capital_case():
    assert capital_case('semaphor') == 'Semaphor'

@qase.id(2)
def test_capital_case2():
    assert capital_case('semaphor') == 'Semaphor'

@qase.id(3)
def test_capital_case3():
    assert capital_case('semaphor') == 'semaphor'