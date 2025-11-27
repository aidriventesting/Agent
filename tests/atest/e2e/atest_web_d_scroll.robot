*** Settings ***
Documentation    E2E test for page scrolling using scroll_down tool
Library    Browser
Resource    ${EXECDIR}/tests/atest/browsers/config.robot

*** Test Cases ***
Test Scroll Down Page
    [Documentation]    Test scrolling down the page using scroll_down tool
    [Tags]    web    scroll    navigation
    Open Website    ${long_page_url}
    Sleep    ${delay}s
    
    Agent.do    instruction=scroll down the page
    Sleep    ${delay}s
    
    Agent.do    instruction=scroll down the page again
    Sleep    ${delay}s
    
    Agent.check    instruction=verify that the page show the following text: This example contains a single test case for user login. It uses a mocked backend api for user management.
    Close Browser

