*** Settings ***
Documentation    E2E test for clear text tool
Library    Browser
Resource    ${EXECDIR}/tests/atest/browsers/config.robot

*** Test Cases ***
Test Clear Text From Input Field
    [Documentation]    Test clearing text from an input field
    [Tags]    web    clear_text    form
    Open Website    ${form_url}
    Sleep    ${delay}s
    
    Agent.do    instruction=type "Hello World" in the textarea field
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that the textarea field have a value which is "Hello World"
    Sleep    ${delay}s

    Agent.do    instruction=clear the textarea field which contains "Hello World"
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that the textarea field is empty
    Sleep    ${delay}s
    Close Browser

