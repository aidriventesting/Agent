*** Settings ***
Documentation    E2E test for browser navigation using go_back tool
Library    Browser
Resource    ${EXECDIR}/tests/atest/config/browsers.robot

*** Test Cases ***
Test Go Back Navigation
    [Documentation]    Test going back in browser history using go_back tool
    [Tags]    web    navigation    go_back
    Open Website    ${home_url}
    Sleep    ${delay}s
    
    Go To    ${form_url}
    Sleep    ${delay}s
    
    Agent.do    instruction=go back to the previous page
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that we are on ${home_url}
    Close Browser

