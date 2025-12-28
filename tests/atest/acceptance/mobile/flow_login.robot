*** Settings ***
Documentation    E2E test for login functionality - Happy path
Library    AppiumLibrary
Library    Agent
Resource    ${EXECDIR}/tests/atest/config/devices.robot

*** Test Cases ***
Test Login Success
    [Documentation]    Happy path: Successful login with valid credentials
    [Tags]    mobile    login
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the LOGIN button
    Sleep    1s
    
    Agent.do    instruction=input admin@gmail.com in the email field
    Sleep    1s
    
    Agent.do    instruction=input admin123 in the password field
    Sleep    1s
    
    Agent.do    instruction=click on the LOGIN button
    Sleep    1s
    
    Agent.check    instruction=verify that we are on screen that displays the text "Enter Admin"
    Sleep    1s
    
    Close Application


Test Login - Wrong Credentials
    [Documentation]    Happy path: Successful login with valid credentials
    [Tags]    mobile    login
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the LOGIN button
    Sleep    1s
    
    Agent.do    instruction=input wrong_email@gmail.com in the email field
    Sleep    1s
    
    Agent.do    instruction=input wrong_password in the password field
    Sleep    1s
    
    Agent.do    instruction=click on the LOGIN button
    Sleep    1s
    
    Agent.check    instruction=verify that the login failed and the error message "Wrong credentials" is displayed
    Sleep    1s
    
    Close Application