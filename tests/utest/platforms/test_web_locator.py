import pytest

pytest.skip("Web support coming soon - web locator not yet implemented", allow_module_level=True)

from Agent.platforms.locators.web import WebLocatorBuilder


@pytest.fixture
def builder():
    return WebLocatorBuilder()


def test_build_with_id(builder):
    element = {"resource_id": "email-search", "class_name": "input"}
    locator = builder.build(element)
    assert '[id="email-search"]' in locator


def test_build_with_aria_label(builder):
    element = {"aria_label": "Search emails", "class_name": "input"}
    locator = builder.build(element)
    assert '[aria-label="Search emails"]' in locator


def test_build_with_placeholder(builder):
    element = {"placeholder": "Search products...", "class_name": "input"}
    locator = builder.build(element)
    assert '[placeholder="Search products..."]' in locator


def test_build_with_text(builder):
    element = {"text": "Add to Cart", "class_name": "button"}
    locator = builder.build(element)
    assert ':text-is("Add to Cart")' in locator


def test_build_with_name(builder):
    element = {"name": "username", "class_name": "input"}
    locator = builder.build(element)
    assert '[name="username"]' in locator


def test_build_with_role(builder):
    element = {"role": "button", "text": "Submit"}
    locator = builder.build(element)
    assert '[role="button"]' in locator


def test_build_combined_attributes(builder):
    element = {
        "resource_id": "submit-btn",
        "class_name": "button",
        "aria_label": "Submit form",
        "text": "Submit"
    }
    locator = builder.build(element)
    assert '[id="submit-btn"]' in locator
    assert '[aria-label="Submit form"]' in locator


def test_build_fails_without_attributes(builder):
    with pytest.raises(AssertionError):
        builder.build({})


def test_build_with_href(builder):
    element = {"class_name": "a", "href": "/products/electronics", "text": "Electronics"}
    locator = builder.build(element)
    assert 'a' in locator
