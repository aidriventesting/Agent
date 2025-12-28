*** Settings ***
Documentation    E2E test for hover tool
Library    Browser
Resource    ${EXECDIR}/tests/atest/config/browsers.robot

*** Test Cases ***
Test Hover Over Element
    [Documentation]    Test hovering over an element to reveal hidden content
    [Tags]    web    hover    interaction
    Open Website    ${form_url}
    Sleep    ${delay}s
    
    Agent.do    instruction=hover over the dropdown select menu
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that the dropdown menu is visible or highlighted
    Sleep    ${delay}s
    Close Browser

