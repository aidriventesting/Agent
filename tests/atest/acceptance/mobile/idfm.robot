*** Settings ***
Documentation    E2E test for IDFM - Happy path
Library    AppiumLibrary
Library    Agent
Resource    ${EXECDIR}/tests/atest/config/devices.robot


*** Test Cases ***
Test IDFM
    [Documentation]    Happy path: Navigate between HOME, SPORT, and MOVIE tabs
    [Tags]    mobile    navigation
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the TAB ACTIVITY button
    Sleep    1s
    
    Agent.check    instruction=verify that the HOME tab is selected and Home fragment text is displayed
    Sleep    1s