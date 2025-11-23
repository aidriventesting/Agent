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
    Sleep    2s
    
    Agent.do    instruction=click on the LONG CLICK button
    Sleep    2s
    
    Agent.check    instruction=verify that the Long Click screen is displayed
    Sleep    1s
    
    Agent.do    instruction=perform a long press on an element or button
    Sleep    2s
    
    Run Keyword And Expect Error    *    Agent.check    instruction=verify the display of the text Get your password and submit button
    Sleep    1s
    
    Close Application
