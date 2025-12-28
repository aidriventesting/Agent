*** Settings ***
Documentation    E2E tests for web vision mode on real-world websites
Resource    ${EXECDIR}/tests/atest/config/browsers.robot


*** Test Cases ***
Test Click Wikipedia Link
    [Documentation]    Test clicking a link on Wikipedia homepage using vision mode
    [Tags]    vision    web    click
    
    Open Website    https://www.wikipedia.org/
    Sleep    2s
    
    Agent.Do    click on English language 
    Sleep    1s

    agent.do    click on the search input fields

    agent.do    type "Robot Framework" in the search input fields

Test Search On DuckDuckGo
    [Documentation]    Test searching on DuckDuckGo using vision mode
    [Tags]    vision    web    input    search
    
    Open Website    https://duckduckgo.com/
    Sleep    2s
    
    Agent.Do    type 'robot framework' in the search box
    Sleep    1s
    
    Agent.Do    click on search button
    Sleep    2s
    
    Get Url    should contain    q=robot

Test Navigate GitHub
    [Documentation]    Test navigating GitHub homepage using vision mode
    [Tags]    vision    web    navigation
    
    Open Website    https://github.com/
    Sleep    2s
    
    Agent.Do    click on Sign in button
    Sleep    1s
    
    Get Url    should contain    login

Test Click Google Search Button
    [Documentation]    Test clicking Google search button using vision mode
    [Tags]    vision    web    click
    
    Open Website    https://www.google.com/
    Sleep    2s
    
    # Accept cookies if present (might fail, that's ok)
    Run Keyword And Ignore Error    Agent.Do    click on Accept all button
    Sleep    1s
    
    Agent.Do    click on search box
    Sleep    0.5s
    
    Get Title    should contain    Google
