import pytest
from Agent.ai.prompts.renderer import UIRenderer


@pytest.fixture
def renderer():
    return UIRenderer()


@pytest.fixture
def web_elements():
    return [
        {
            "class_name": "button",
            "type": "submit",
            "aria_label": "Submit form",
            "placeholder": "",
            "text": "Submit",
            "resource_id": "submit-btn",
            "name": "submit"
        },
        {
            "class_name": "input",
            "type": "email",
            "aria_label": "",
            "placeholder": "Enter email",
            "text": "",
            "resource_id": "email",
            "name": "email"
        }
    ]


@pytest.fixture
def android_elements():
    return [
        {
            "text": "Login",
            "resource_id": "com.app:id/login",
            "accessibility_label": "Login button",
            "class_name": "android.widget.Button"
        },
        {
            "text": "",
            "resource_id": "com.app:id/email",
            "accessibility_label": "Email input",
            "class_name": "android.widget.EditText"
        }
    ]


@pytest.fixture
def ios_elements():
    return [
        {
            "text": "Login",
            "resource_id": "loginBtn",
            "accessibility_label": "Login",
            "class_name": "XCUIElementTypeButton"
        },
        {
            "text": "",
            "resource_id": "emailField",
            "accessibility_label": "Email",
            "class_name": "XCUIElementTypeTextField"
        }
    ]


def test_render_empty(renderer):
    result = renderer.render([], platform="web")
    assert result == "(no UI elements found)"


def test_render_web_elements(renderer, web_elements):
    result = renderer.render(web_elements, platform="web")
    assert "1." in result
    assert "2." in result
    assert "Submit" in result
    assert "placeholder='Enter email'" in result


def test_render_web_includes_aria_label(renderer, web_elements):
    result = renderer.render(web_elements, platform="web")
    assert "aria-label='Submit form'" in result


def test_render_android_elements(renderer, android_elements):
    result = renderer.render(android_elements, platform="android")
    assert "1." in result
    assert "Login" in result
    assert "content-desc='Login button'" in result


def test_render_ios_elements(renderer, ios_elements):
    result = renderer.render(ios_elements, platform="ios")
    assert "1." in result
    assert "Login" in result
    assert "name='loginBtn'" in result
    assert "label='Login'" in result


def test_render_respects_max_items(renderer):
    elements = [{"text": f"Element {i}", "class_name": "button"} for i in range(200)]
    result = renderer.render(elements, platform="web")
    lines = [l for l in result.split('\n') if l.strip()]
    assert len(lines) == 150


def test_render_mobile_max_items(renderer):
    elements = [{"text": f"Element {i}", "class_name": "Button"} for i in range(100)]
    result = renderer.render(elements, platform="android")
    lines = [l for l in result.split('\n') if l.strip()]
    assert len(lines) == 50
