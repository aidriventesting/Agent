*** Settings ***
Documentation    Simple vision mode tests for basic web interactions
Resource    ${EXECDIR}/tests/atest/browsers/config.robot
Suite Setup    Open Website
Suite Teardown    Close Browser

*** Test Cases ***
Test Click Simple Button
    [Documentation]    Test clicking a simple button using vision mode
    [Tags]    vision    web    click    basic
    
    Go To    https://the-internet.herokuapp.com/
    Sleep    ${short_wait}
    
    Agent.Do    click on Add/Remove Elements link
    Sleep    ${veryShort_wait}
    
    Get Url    *=    add_remove_elements

Test Click And Verify
    [Documentation]    Test clicking and verifying result using vision mode
    [Tags]    vision    web    click    verify
    
    Go To    https://the-internet.herokuapp.com/add_remove_elements/
    Sleep    ${short_wait}
    
    Agent.Do    click on Add Element button
    Sleep    ${veryShort_wait}
    
    # Verify button was added
    Agent.check    instruction=verify that a button delete is displayed

Test Hover Over Element
    [Documentation]    Test hovering over an element using vision mode
    [Tags]    vision    web    hover
    
    Go To    https://the-internet.herokuapp.com/hovers
    Sleep    ${short_wait}
    
    Agent.Do    hover over the first image
    Sleep    ${veryShort_wait}
    
    # Verify hover text appears
    Agent.check    instruction=verify that the hover text "name: user1" is displayed

Test Navigate Back
    [Documentation]    Test navigation using vision mode
    [Tags]    vision    web    navigation
    
    Go To    https://the-internet.herokuapp.com/
    Sleep    ${short_wait}
    
    Agent.Do    click on Checkboxes link
    Sleep    ${veryShort_wait}
    
    Agent.Do    go back
    Sleep    ${veryShort_wait}
    
    Get Url    ==    https://the-internet.herokuapp.com/
