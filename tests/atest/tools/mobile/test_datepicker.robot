*** Settings ***
Documentation    E2E tests for Date picker - Happy paths
Library    AppiumLibrary
Library    Agent
Library    DateTime
Resource    ${EXECDIR}/tests/atest/config/devices.robot

*** Keywords ***
Get Current Date Plus Days
    [Documentation]    Returns current date with added days
    [Arguments]    ${days}
    # Get current datetime without formatting, add days, then format
    ${current_datetime} =    Get Current Date
    ${new_datetime} =    Add Time To Date    ${current_datetime}    ${days} days
    ${new_date} =    Convert Date    ${new_datetime}    result_format=%B %d, %Y
    ${current_date} =    Convert Date    ${current_datetime}    result_format=%B %d, %Y
    Log    Original date: ${current_date}
    Log    Date + ${days} days: ${new_date}
    RETURN    ${new_date}

*** Test Cases ***
Test Date Picker Display
    [Documentation]    Happy path: Verify current date is displayed
    [Tags]    mobile    pickers    date
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the DATE button
    Sleep    1s
    
    Agent.check    instruction=verify that the Date Activity screen is displayed with a calendar
    Sleep    1s
    
    ${current_date} =    Get Current Date    result_format=%B %d, %Y
    Agent.check    instruction=verify that the current date ${current_date} is displayed or highlighted
    Sleep    1s
    
    Close Application

Test Date Picker Display Negative
    [Documentation]    Negative test: Verify wrong date is NOT displayed
    [Tags]    mobile    pickers    date    negative
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the DATE button
    Sleep    1s
    
    Agent.check    instruction=verify that the Date Activity screen is displayed with a calendar
    Sleep    1s
    
    # Get current date + 7 days (wrong date)
    ${wrong_date} =    Get Current Date Plus Days    7
    
    Run Keyword And Expect Error    *    Agent.check    instruction=verify that the date ${wrong_date} is currently selected or highlighted
    Sleep    1s
    
    Close Application
