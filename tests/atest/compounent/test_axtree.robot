*** Settings ***
Documentation    Test AXTree collector strategy for UI element collection
Library          Browser
Library          Agent.platforms._webconnector.WebConnectorRF    axtree    AS    Connector
Library          tests/atest/compounent/BBoxVisualizer.py


*** Test Cases ***
Test AXTree Collector On Simple Login Form
    [Documentation]    Test AXTree collector on a simple login form
    [Tags]    collector    axtree    login
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://the-internet.herokuapp.com/login
    
    ${elements}=    Connector.Collect UI Candidates
    Log    \n=== AXTREE COLLECTOR ===
    Log    Found ${elements.__len__()} elements
    
    Log Many    @{elements}
    
    Should Not Be Empty    ${elements}
    Should Be True    ${elements.__len__()} >= 3
    
    [Teardown]    Close Browser


Test AXTree Collector On SauceDemo
    [Documentation]    Test AXTree collector on SauceDemo login page
    [Tags]    collector    axtree    saucedemo
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://www.saucedemo.com
    
    ${elements}=    Connector.Collect UI Candidates
    Log    \n=== AXTREE COLLECTOR (SauceDemo) ===
    Log    Found ${elements.__len__()} elements
    
    Log Many    @{elements}
    
    # Should find at least username, password, and login button
    Should Not Be Empty    ${elements}
    Should Be True    ${elements.__len__()} >= 3
    
    [Teardown]    Close Browser


Test AXTree Collector Element Details
    [Documentation]    Verify that AXTree collector captures all required attributes
    [Tags]    collector    axtree    details
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://the-internet.herokuapp.com/login
    
    ${elements}=    Connector.Collect UI Candidates
    
    # Verify first element has expected keys
    ${first_element}=    Set Variable    ${elements}[0]
    Should Contain    ${first_element}    text
    Should Contain    ${first_element}    resource_id
    Should Contain    ${first_element}    content_desc
    Should Contain    ${first_element}    class_name
    Should Contain    ${first_element}    role
    Should Contain    ${first_element}    clickable
    Should Contain    ${first_element}    enabled
    
    Log    \n=== First Element Details ===
    Log    ${first_element}
    
    [Teardown]    Close Browser


Test AXTree With BBox Visualization
    [Documentation]    Visualize AXTree bounding boxes on screenshot
    [Tags]    collector    axtree    visualization    bbox
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://the-internet.herokuapp.com/login
    
    # Collect elements
    ${elements}=    Connector.Collect UI Candidates
    Log    Found ${elements.__len__()} accessible elements with bounding boxes
    
    # Take screenshot
    ${screenshot}=    Take Screenshot    filename=axtree_original.png    fullPage=True
    
    # Draw bounding boxes and embed in log
    ${annotated}=    Draw And Log Elements    ${elements}    ${screenshot}
    
    Log    ✅ AXTree annotated screenshot saved: ${annotated}
    Log    📦 Total accessible elements annotated: ${elements.__len__()}
    
    Should Not Be Empty    ${annotated}
    
    [Teardown]    Close Browser

