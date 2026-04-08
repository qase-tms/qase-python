"""Tests demonstrating tags support."""
from qase.pytest import qase


@qase.id(901)
@qase.title("Test with single tag")
@qase.tags("smoke")
def test_single_tag():
    assert True


@qase.id(902)
@qase.title("Test with multiple tags")
@qase.tags("smoke", "regression", "api")
def test_multiple_tags():
    assert True


@qase.id(903)
@qase.title("Test with tags via fields")
@qase.fields(("tags", "fromfield"))
def test_tags_via_fields():
    assert True


@qase.id(904)
@qase.title("Test with merged tags")
@qase.tags("api")
@qase.fields(("tags", "fromfield"))
def test_tags_merged():
    assert True
