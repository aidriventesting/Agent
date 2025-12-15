*** Settings ***
Documentation    Tests for Agent.Ask keyword
Resource    ../browsers/config.robot
Test Setup    Open Website    https://agent-arena-eta.vercel.app/v1/
Test Teardown    Close Browser

*** Test Cases ***
Ask About Page Title
    [Documentation]    Ask AI about the page title
    ${response}=    Agent.Ask    What is the main title or heading of this page?
    Log    AI Response: ${response}
    Should Not Be Empty    ${response}

Ask For JSON Response
    [Documentation]    Ask AI for structured JSON response
    ${response}=    Agent.Ask    List the navigation menu items you can see    format=json
    Log    AI Response: ${response}
    Should Not Be Empty    ${response}
    Should Contain    ${response}    {
