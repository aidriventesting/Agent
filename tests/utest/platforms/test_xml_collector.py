import pytest
import os
from Agent.platforms.collectors.xml_collector import XMLCollector


@pytest.fixture
def android_collector():
    return XMLCollector(platform="android")


@pytest.fixture
def ios_collector():
    return XMLCollector(platform="ios")


@pytest.fixture
def facebook_login_xml():
    xml_path = os.path.join(os.path.dirname(__file__), "../../_data/mobileuihierarchy/facebook-login-screen.xml")
    if not os.path.exists(xml_path):
        xml_path = "tests/_data/mobileuihierarchy/facebook-login-screen.xml"
    with open(xml_path, 'r') as f:
        return f.read()


@pytest.fixture
def facebook_createaccount_xml():
    xml_path = os.path.join(os.path.dirname(__file__), "../../_data/mobileuihierarchy/facebook-createaccount-screen.xml")
    if not os.path.exists(xml_path):
        xml_path = "tests/_data/mobileuihierarchy/facebook-createaccount-screen.xml"
    with open(xml_path, 'r') as f:
        return f.read()


def test_parse_facebook_login_xml(android_collector, facebook_login_xml):
    elements = android_collector.parse_xml(facebook_login_xml)
    assert len(elements) > 0
    
    username_field = [e for e in elements if e.get('accessibility_label') == "Nom d'utilisateur"]
    assert len(username_field) == 1
    assert username_field[0]['clickable'] == True
    
    password_field = [e for e in elements if e.get('accessibility_label') == 'Mot de passe']
    assert len(password_field) == 1
    assert password_field[0]['clickable'] == True
    
    login_btn = [e for e in elements if e.get('accessibility_label') == 'Se connecter']
    assert len(login_btn) == 1
    assert login_btn[0]['clickable'] == True


def test_parse_facebook_createaccount_xml(android_collector, facebook_createaccount_xml):
    elements = android_collector.parse_xml(facebook_createaccount_xml)
    assert len(elements) > 0
    
    back_btn = [e for e in elements if e.get('accessibility_label') == 'Retour']
    assert len(back_btn) == 1
    assert back_btn[0]['clickable'] == True
    
    next_btn = [e for e in elements if e.get('text') == 'Suivant']
    assert len(next_btn) == 1
    assert next_btn[0]['clickable'] == True
    
    title = [e for e in elements if e.get('text') == 'Créer un compte']
    assert len(title) == 1


def test_parse_android_bounds(android_collector):
    bbox = android_collector._parse_android_bounds("[100,200][300,250]")
    assert bbox == {'x': 100, 'y': 200, 'width': 200, 'height': 50}


def test_parse_android_bounds_invalid(android_collector):
    assert android_collector._parse_android_bounds("") == {}
    assert android_collector._parse_android_bounds("invalid") == {}


def test_set_platform():
    collector = XMLCollector(platform="android")
    assert collector._platform == "android"
    
    collector.set_platform("ios")
    assert collector._platform == "ios"


def test_get_name(android_collector):
    assert android_collector.get_name() == "xml"
