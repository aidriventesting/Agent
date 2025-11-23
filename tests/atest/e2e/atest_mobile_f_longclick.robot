*** Settings ***
Documentation    E2E tests for advanced interactions - Happy paths
Library    AppiumLibrary
Library    Agent
Resource    ${EXECDIR}/tests/atest/devices/config.robot

*** Test Cases ***
Test Long Click
    [Documentation]    Happy path: Perform long click on an element
    ...    currently long click is not implemented
    [Tags]    mobile    interactions    longclick
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the LONG CLICK button
    Sleep    1s
    
    Agent.check    instruction=verify that the popup "Get your password" is displayed with the email field, CANCEL button, and SUBMIT button
    Sleep    1s
    
    Agent.do    instruction=click on the CANCEL button
    Sleep    1s
    
    Run Keyword And Expect Error    *    Agent.check    instruction=verify that the popup "Get your password" is displayed with the email field, CANCEL button, and SUBMIT button
    Sleep    1s
    
    Close Application
