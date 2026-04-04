"""Tests demonstrating suite organization."""
from qase.pytest import qase


@qase.id(301)
@qase.title("Test in Authentication suite")
@qase.suite("Authentication")
def test_auth_suite():
    assert True


@qase.id(302)
@qase.title("Test in nested Authentication.OAuth suite")
@qase.suite("Authentication.OAuth")
def test_nested_suite():
    assert True


@qase.id(303)
@qase.title("Test in deeply nested suite")
@qase.suite("Authentication.OAuth.Google")
def test_deep_nested_suite():
    assert True
