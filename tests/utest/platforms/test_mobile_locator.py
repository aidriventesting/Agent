import pytest
from Agent.platforms.locators.mobile import MobileLocatorBuilder


@pytest.fixture
def android_builder():
    return MobileLocatorBuilder(platform="android")


@pytest.fixture
def ios_builder():
    return MobileLocatorBuilder(platform="ios")


# Android tests
def test_android_id(android_builder):
    element = {"resource_id": "com.app:id/login_button"}
    assert android_builder.build(element) == "id=com.app:id/login_button"


def test_android_accessibility_id(android_builder):
    element = {"accessibility_label": "Login"}
    assert android_builder.build(element) == "accessibility_id=Login"


def test_android_content_desc_fallback(android_builder):
    element = {"content_desc": "Submit button"}
    assert android_builder.build(element) == "accessibility_id=Submit button"


def test_android_text_xpath(android_builder):
    element = {"text": "Sign In"}
    assert android_builder.build(element) == "//*[@text='Sign In']"


def test_android_class(android_builder):
    element = {"class_name": "android.widget.Button"}
    assert android_builder.build(element) == "class=android.widget.Button"


# iOS tests
def test_ios_id(ios_builder):
    element = {"resource_id": "loginButton"}
    assert ios_builder.build(element) == "id=loginButton"


def test_ios_accessibility_id(ios_builder):
    element = {"accessibility_label": "Login"}
    assert ios_builder.build(element) == "accessibility_id=Login"


def test_ios_label_fallback(ios_builder):
    element = {"label": "Submit"}
    assert ios_builder.build(element) == "accessibility_id=Submit"


def test_ios_text_predicate(ios_builder):
    element = {"text": "Sign In"}
    locator = ios_builder.build(element)
    assert "-ios predicate string:" in locator
    assert "label == 'Sign In'" in locator


def test_ios_class(ios_builder):
    element = {"class_name": "XCUIElementTypeButton"}
    assert ios_builder.build(element) == "class=XCUIElementTypeButton"


# Platform switching
def test_set_platform():
    builder = MobileLocatorBuilder(platform="android")
    assert builder.build({"text": "Test"}) == "//*[@text='Test']"
    
    builder.set_platform("ios")
    locator = builder.build({"text": "Test"})
    assert "-ios predicate string:" in locator


def test_fails_without_attributes():
    builder = MobileLocatorBuilder()
    with pytest.raises(AssertionError):
        builder.build({})
