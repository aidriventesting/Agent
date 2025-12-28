*** Settings ***
Documentation    E2E test for Contact Us form - Happy path
Library    AppiumLibrary
Library    Agent
Resource    ${EXECDIR}/tests/atest/config/devices.robot

*** Test Cases ***
Test Contact Us Form Submit
    [Documentation]    Happy path: Fill and submit Contact Us form
    [Tags]    mobile    forms
    Open Application With Config
    Sleep    1s
    
    Agent.do    instruction=click on the CONTACT US FORM button
    Sleep    1s
    
    Agent.do    instruction=input Abdelkader in the name field
    Sleep    1s
    
    Agent.do    instruction=input abdelkader@gmail.com in the email field
    Sleep    1s
    
    Agent.do    instruction=input 123 Rue de la Paix, Paris in the address field
    Sleep    1s
    
    Agent.do    instruction=input 1234567890 in the mobile number field
    Sleep    1s
    
    Agent.do    instruction=click on the SUBMIT button
    Sleep    1s
    
    Agent.check    instruction=verify that the form was submitted successfully and show the following information : Abdelkader, abdelkader@gmail.com, 123 Rue de la Paix, Paris, 1234567890
    Sleep    1s
    
    Close Application
