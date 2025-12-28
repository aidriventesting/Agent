*** Settings ***
Documentation    E2E test for keyboard key press using press_key tool
Library    Browser
Resource    ${EXECDIR}/tests/atest/config/browsers.robot

*** Test Cases ***
Test Press Enter Key To Submit
    [Documentation]    Test pressing Enter key to submit form
    [Tags]    web    keyboard    press_key
    Open Website    ${form_url}
    Sleep    ${delay}s
    
    Agent.do    instruction=type "Test Input" in textarea input field
    Sleep    ${delay}s
    
    Agent.do    instruction=press Enter key to submit
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that the Textarea input field have a value which is "Test Input"
    Close Browser
