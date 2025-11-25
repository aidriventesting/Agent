*** Settings ***
Documentation    E2E test for double click tool
Library    Browser
Resource    ${EXECDIR}/tests/atest/browsers/config.robot

*** Test Cases ***
Test Double Click On Element
    [Documentation]    Test double clicking an element
    [Tags]    web    double_click    interaction
    Open Website    ${form_url}
    Sleep    ${delay}s
    
    Agent.do    instruction=double click on Color picker
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that the Color picker element is open you see the color palette on the screenshot
    Sleep    ${delay}s
    Close Browser

