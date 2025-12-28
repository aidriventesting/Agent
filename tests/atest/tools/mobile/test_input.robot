*** Settings ***
Documentation    E2E test for basic form interaction - Happy path
Library    AppiumLibrary
Library    Agent
Resource    ${EXECDIR}/tests/atest/config/devices.robot

*** Test Cases ***
Test Basic Form Input And Submit
    [Documentation]    Happy path: Enter text in form and verify submission
    [Tags]    mobile    form    basic
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the button enter some value
    Sleep    1s
    
    Agent.do    instruction=input this text in the text field: hello
    Sleep    1s
    
    Agent.do    instruction=click on the submit button
    Sleep    1s
    
    Agent.check    instruction=verify that the text hello is displayed under the submit button
    Sleep    1s
    
    Close Application