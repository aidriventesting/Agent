*** Settings ***
Documentation    E2E test for ScrollView - Happy path
Library    AppiumLibrary
Library    Agent
Resource    ${EXECDIR}/tests/atest/config/devices.robot

*** Test Cases ***
Test ScrollView Scroll Positif - Correct Buttons Display
    [Documentation]    Happy path: Scroll down to see more buttons
    [Tags]    mobile    scrollview    positif
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the ScrollView button
    Sleep    1s
    
    Agent.check    instruction=verify that the ScrollView title is displayed and initial buttons like BUTTON1 are visible
    Sleep    1s
    
    Agent.do    instruction=scroll down to see more buttons
    Sleep    1s
    
    Agent.check    instruction=verify that more buttons like BUTTON14, BUTTON15, BUTTON16 are visible
    Sleep    1s
    
    Close Application


Test ScrollView Scroll Negative - Wrong Buttons Display
    [Documentation]    Negative test: Verify wrong buttons are not displayed
    [Tags]    mobile    scrollview    negative
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the ScrollView button
    Sleep    1s
    
    Agent.check    instruction=verify that the ScrollView title is displayed and initial buttons like BUTTON1 are visible
    Sleep    1s
    
    Agent.do    instruction=scroll down to see more buttons
    Sleep    1s
    
    Run Keyword And Expect Error    *    Agent.check    instruction=verify that the following buttons are visible: BUTTON1, BUTTON2, BUTTON3 
    Sleep    1s
    
    Close Application