*** Settings ***
Documentation    E2E test for Agent Arena benchmark - Tests different element_source and selection_mode combinations
...              Website: https://agent-arena-eta.vercel.app/webarena/c0/
...    
...              Run all combinations:
...                  robot tests/atest/e2e/atest_web_arena_benchmark.robot
...    
...              Run specific combination:
...                  robot --include som tests/atest/e2e/atest_web_arena_benchmark.robot
...                  robot --include text tests/atest/e2e/atest_web_arena_benchmark.robot
Resource    ${EXECDIR}/tests/atest/config/browsers.robot
Test Template    Run Arena Test

*** Variables ***
${ARENA_URL}    https://agent-arena-eta.vercel.app/webarena/c0/feed.html
${DELAY}        2

*** Test Cases ***                  ELEMENT_SOURCE    SELECTION_MODE
Text + Tree (default)               tree              text
    [Tags]    text    tree

SoM + Tree                          tree              som
    [Tags]    som    tree

Visual Only                         visual            som
    [Tags]    visual

*** Keywords ***
Run Arena Test
    [Documentation]    Execute the arena benchmark test with specified modes
    [Arguments]    ${element_source}    ${selection_mode}
    
    Log    Testing: element_source=${element_source}, selection_mode=${selection_mode}    console=True
    
    ${agent}=    Get Library Instance    Agent
    Call Method    ${agent.engine}    set_element_source    ${element_source}
    Call Method    ${agent.engine}    set_selection_mode    ${selection_mode}
    
    Open Website    ${ARENA_URL}
    Sleep    ${DELAY}s
    
    # Test 1: Navigate via sidebar
    Agent.do    instruction=click on Messages in the left sidebar
    Sleep    ${DELAY}s
    
    # Test 2: Navigate to notifications
    Agent.do    instruction=Click on Emma Laurent
    Sleep    ${DELAY}s
    
    # Test 3: Return to feed
    Agent.do    instruction=Input text message "Hello Emma, how are you?" in the input field
    Sleep    ${DELAY}s
    
    # Test 4: Interact with post
    Agent.do    instruction=Click the button send to send the message
    Sleep    ${DELAY}s
    
    # Test 5: Add friend
    Agent.Check    instruction=Check if the message "Hello Emma, how are you?" is displayed in the conversation with Emma Laurent
    Sleep    ${DELAY}s
    
    [Teardown]    Close Browser
