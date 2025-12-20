*** Settings ***
Documentation    E2E test for basic web form interaction - Happy path
Resource    ${EXECDIR}/tests/atest/config/browsers.robot

*** Test Cases ***
Test Basic Form Input And Submit
    [Documentation]    Happy path: Enter text in form and verify submission
    [Tags]    web    form    basic
    Open Website    ${form_url}
    Sleep    ${delay}s
    
    Agent.do    instruction=type "Text input" in the text input field
    Sleep    ${delay}s
    
    Agent.do    instruction=fill the password field with "test123"
    Sleep    ${delay}s
    
    Agent.do    instruction=click the submit button
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that the page shows a success or confirmation message
    Sleep    ${delay}s
    Close Browser

