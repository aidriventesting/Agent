*** Settings ***
Documentation    E2E test for scroll up tool
Library    Browser
Resource    ${EXECDIR}/tests/atest/config/browsers.robot

*** Test Cases ***
Test Scroll Up Page
    [Documentation]    Test scrolling up the page
    [Tags]    web    scroll    navigation
    Open Website    ${long_page_url}
    Sleep    ${delay}s
    
    # First scroll down
    Agent.do    instruction=scroll down the page
    Sleep    ${delay}s
    
    # Then scroll back up
    Agent.do    instruction=scroll up the page
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that we are at the top of the page
    Sleep    ${delay}s
    Close Browser

