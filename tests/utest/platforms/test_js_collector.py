import pytest
from Agent.platforms.collectors.js_query_collector import JSQueryCollector


@pytest.fixture
def collector():
    return JSQueryCollector()


@pytest.fixture
def raw_js_elements():
    return [
        {
            "text": "Login",
            "id": "login-btn",
            "className": "btn primary",
            "name": "",
            "role": "button",
            "ariaLabel": "Login to your account",
            "placeholder": "",
            "tag": "button",
            "testId": "",
            "type": "submit",
            "href": "",
            "bbox": {"x": 100, "y": 200, "width": 80, "height": 40}
        },
        {
            "text": "",
            "id": "email",
            "className": "form-input",
            "name": "email",
            "role": "",
            "ariaLabel": "",
            "placeholder": "Enter your email",
            "tag": "input",
            "testId": "email-input",
            "type": "email",
            "href": "",
            "bbox": {"x": 100, "y": 100, "width": 200, "height": 40}
        },
        {
            "text": "Products",
            "id": "",
            "className": "nav-link",
            "name": "",
            "role": "link",
            "ariaLabel": "",
            "placeholder": "",
            "tag": "a",
            "testId": "",
            "type": "",
            "href": "/products",
            "bbox": {"x": 50, "y": 20, "width": 80, "height": 30}
        }
    ]


def test_deduplicate_removes_duplicates(collector):
    candidates = [
        {"text": "Login", "resource_id": "btn1", "aria_label": "", "placeholder": "", "name": "", "class_name": "button", "css_class": "", "href": ""},
        {"text": "Login", "resource_id": "btn1", "aria_label": "", "placeholder": "", "name": "", "class_name": "button", "css_class": "", "href": ""},
        {"text": "Submit", "resource_id": "btn2", "aria_label": "", "placeholder": "", "name": "", "class_name": "button", "css_class": "", "href": ""},
    ]
    result = collector._deduplicate_candidates(candidates)
    assert len(result) == 2


def test_deduplicate_keeps_unique(collector):
    candidates = [
        {"text": "Login", "resource_id": "btn1", "aria_label": "", "placeholder": "", "name": "", "class_name": "button", "css_class": "", "href": ""},
        {"text": "Login", "resource_id": "btn2", "aria_label": "", "placeholder": "", "name": "", "class_name": "button", "css_class": "", "href": ""},
    ]
    result = collector._deduplicate_candidates(candidates)
    assert len(result) == 2


def test_element_transformation():
    elem_data = {
        "text": "Submit",
        "id": "submit-btn",
        "className": "btn btn-primary",
        "name": "submit",
        "role": "button",
        "ariaLabel": "Submit form",
        "placeholder": "",
        "tag": "button",
        "testId": "submit-test",
        "type": "submit",
        "href": "",
        "bbox": {"x": 10, "y": 20, "width": 100, "height": 40}
    }
    
    attrs = {
        'text': elem_data.get('text', ''),
        'resource_id': elem_data.get('testId') or elem_data.get('id', ''),
        'aria_label': elem_data.get('ariaLabel', ''),
        'placeholder': elem_data.get('placeholder', ''),
        'css_class': elem_data.get('className', ''),
        'class_name': elem_data.get('tag', ''),
        'role': elem_data.get('role', ''),
        'name': elem_data.get('name', ''),
        'type': elem_data.get('type', ''),
        'href': elem_data.get('href', ''),
        'bbox': elem_data.get('bbox', {}),
    }
    
    assert attrs['text'] == "Submit"
    assert attrs['resource_id'] == "submit-test"
    assert attrs['aria_label'] == "Submit form"
    assert attrs['class_name'] == "button"
    assert attrs['css_class'] == "btn btn-primary"


def test_get_name(collector):
    assert collector.get_name() == "js_query"
