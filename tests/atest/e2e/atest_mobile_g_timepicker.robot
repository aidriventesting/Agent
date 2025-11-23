*** Settings ***
Documentation    E2E tests for Time picker - Happy paths
Library    AppiumLibrary
Library    Agent
Library    DateTime
Resource    ${EXECDIR}/tests/atest/devices/config.robot

*** Keywords ***
Get Device Time Plus Hours
    [Documentation]    Returns device time with added hours
    [Arguments]    ${hours}
    # Get current datetime and add hours
    ${current_datetime} =    Get Current Date
    ${new_datetime} =    Add Time To Date    ${current_datetime}    ${hours} hours
    ${new_time} =    Convert Date    ${new_datetime}    result_format=%H:%M
    Log    New time (+ ${hours}h): ${new_time}
    RETURN    ${new_time}

*** Test Cases ***
Test Time Picker Display Positif - Correct Time Correct AM/PM
    [Documentation]    Happy path: Select a time in the Time picker
    [Tags]    mobile    pickers    time
    Open Application With Config
    Sleep    2s
    
    Agent.do    instruction=click on the TIME button
    Sleep    2s
    
    Agent.check    instruction=verify that the Time picker is displayed
    Sleep    1s
    
    ${device_time} =    Get Device Time    HH:mm
    Agent.check    instruction=verify that time displayed on the screen is ${device_time} without caring about the AM/PM
    Sleep    1s
    
    Close Application

Test Time Picker Display Negative - Correct Time Wrong AM/PM
    [Documentation]    Negative test: Verify wrong time is displayed
    [Tags]    mobile    pickers    time    negative   high_precision
    Open Application With Config
    Sleep    2s
    
    Agent.do    instruction=click on the TIME button
    Sleep    2s
    
    Agent.check    instruction=verify that the Time picker is displayed
    Sleep    1s
    
    ${device_time} =    Get Device Time    HH:mm
    Run Keyword And Expect Error    *    Agent.check    instruction=verify that time displayed on the screen is ${device_time}
    Sleep    1s
    
    Close Application

Test Time Picker Display Negative - Wrong Time 
    [Documentation]    Negative test: Verify wrong time is NOT displayed
    [Tags]    mobile    pickers    time    negative
    Open Application With Config
    Sleep    2s
    
    Agent.do    instruction=click on the TIME button
    Sleep    2s
    
    Agent.check    instruction=verify that the Time picker is displayed
    Sleep    1s
    
    # Get device time + 1 hour (wrong time)
    ${wrong_time} =    Get Device Time Plus Hours    1
    
    Run Keyword And Expect Error    *    Agent.check    instruction=verify that the time displayed on the screen is ${wrong_time} without caring about the AM/PM
    Sleep    1s
    
    Close Application