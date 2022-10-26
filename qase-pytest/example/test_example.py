from qaseio.pytest import qase


def capital_case(x):
    return x.capitalize()

@qase.title('Test should pass')
def test_capital_case():
    assert capital_case('semaphor') == 'Semaphor'


@qase.title("Test should fail")
def test_capital_case2():
    assert capital_case('semaphor') == 'semaphor'