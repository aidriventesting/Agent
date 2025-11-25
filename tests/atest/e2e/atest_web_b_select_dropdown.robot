*** Settings ***
Documentation    E2E test for dropdown selection using select_option tool
Library    Browser
Resource    ${EXECDIR}/tests/atest/browsers/config.robot

*** Test Cases ***
Test Select Option From Dropdown
    [Documentation]    Test selecting an option from dropdown using select_option tool
    [Tags]    web    dropdown    select
    Open Website    ${form_url}
    Sleep    ${delay}s
    
    Agent.do    instruction=select the second option from the dropdown
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that the Dropdown (select) element display the selected option "Two" and the the Dropdown (datalist) displys a placeholder "Type to search..."
    Sleep    ${delay}s
    Close Browser

