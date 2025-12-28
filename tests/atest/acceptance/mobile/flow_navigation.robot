*** Settings ***
Documentation    E2E test for tab navigation - Happy path
Library    AppiumLibrary
Library    Agent
Resource    ${EXECDIR}/tests/atest/config/devices.robot

*** Test Cases ***
Test Tab Navigation
    [Documentation]    Happy path: Navigate between HOME, SPORT, and MOVIE tabs
    [Tags]    mobile    navigation
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the TAB ACTIVITY button
    Sleep    1s
    
    Agent.check    instruction=verify that the HOME tab is selected and Home fragment text is displayed
    Sleep    1s
    
    Agent.do    instruction=click on the SPORT tab
    Sleep    1s
    
    Agent.check    instruction=verify that the SPORT tab is selected and Sport fragment text is displayed
    Sleep    1s
    
    Agent.do    instruction=click on the MOVIE tab
    Sleep    1s
    
    Agent.check    instruction=verify that the MOVIE tab is selected and Movie fragment text is displayed
    Sleep    1s
    
    Close Application
