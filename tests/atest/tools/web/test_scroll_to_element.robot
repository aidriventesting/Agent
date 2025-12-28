*** Settings ***
Documentation    E2E test for scroll to element tool
Library    Browser
Resource    ${EXECDIR}/tests/atest/config/browsers.robot

*** Test Cases ***
Test Scroll To Specific Element
    [Documentation]    Test scrolling to a specific element on the page
    [Tags]    web    scroll    element
    Open Website    ${long_page_url}
    Sleep    ${delay}s
    
    Agent.do    instruction=scroll to the Privacy Policy section at the bottom of the page
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that we can see the Privacy Policy in the screenshot
    Sleep    ${delay}s
    Close Browser

