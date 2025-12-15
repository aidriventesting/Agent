*** Settings ***
Documentation    E2E test for Agent Arena benchmark - Tests different click_mode and input_mode combinations
...              Website: https://agent-arena-eta.vercel.app/webarena/c0/
...    
...              Run all combinations:
...                  robot tests/atest/e2e/atest_web_arena_benchmark.robot
...    
...              Run specific combination:
...                  robot --include som tests/atest/e2e/atest_web_arena_benchmark.robot
...                  robot --include text tests/atest/e2e/atest_web_arena_benchmark.robot
Resource    ${EXECDIR}/tests/atest/browsers/config.robot
Test Template    Run Arena Test

*** Variables ***
${ARENA_URL}    https://agent-arena-eta.vercel.app/webarena/c0/feed.html
${DELAY}        2

*** Test Cases ***                  CLICK_MODE    INPUT_MODE
Text + XML (default)                xml           text
    [Tags]    text    xml

SoM + XML                           xml           som
    [Tags]    som    xml

Visual Only                         visual        som
    [Tags]    visual

*** Keywords ***
Run Arena Test
    [Documentation]    Execute the arena benchmark test with specified modes
    [Arguments]    ${click_mode}    ${input_mode}
    
    Log    Testing: click_mode=${click_mode}, input_mode=${input_mode}    console=True
    
    ${agent}=    Get Library Instance    Agent
    Call Method    ${agent.engine}    set_click_mode    ${click_mode}
    Call Method    ${agent.engine}    set_input_mode    ${input_mode}
    
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
