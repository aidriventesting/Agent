*** Settings ***
Documentation    E2E test for Hybrid Activity - Happy path
Library    AppiumLibrary
Library    Agent
Resource    ${EXECDIR}/tests/atest/devices/config.robot

*** Test Cases ***
Test Hybrid Activity
    [Documentation]    Happy path: Interact with Hybrid Activity input field
    [Tags]    mobile    hybrid
    Open Application With Config
    Sleep    2s
    
    Agent.do    instruction=click on the HYBRID button
    Sleep    2s
    
    Agent.check    instruction=verify that the Hybrid Activity screen is displayed with "Hybrid Activity" title
    Sleep    1s
    
    Agent.do    instruction=input some text in the "Enter some Value" field
    Sleep    1s
    
    Agent.do    instruction=click on the SUBMIT button
    Sleep    2s
    
    Agent.check    instruction=verify that the text was submitted or displayed in the preview area
    Sleep    1s
    
    Close Application
