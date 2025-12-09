*** Settings ***
Documentation    Test JSQuery collector strategy for UI element collection
Library          Browser
Library          Agent.platforms._webconnector.WebConnectorRF    js_query    AS    Connector
Library          tests/atest/compounent/BBoxVisualizer.py
Resource         ${EXECDIR}/tests/atest/browsers/config.robot

*** Test Cases ***
Test Herokuapp
    [Documentation]    Test JSQuery collector on a simple login form
    [Tags]    collector    js_query    login
    
    Open Website    https://the-internet.herokuapp.com/login
    
    ${elements}=    Connector.Collect UI Candidates
    Log Many    @{elements}

    ${screenshot}=    Take Screenshot    filename=original.png    fullPage=True
    ${annotated}=    Draw And Log Elements    ${elements}    ${screenshot}
    
    [Teardown]    Close Browser


Test JSQuery Collector On SauceDemo
    [Documentation]    Test JSQuery collector on SauceDemo login page
    [Tags]    collector    js_query    saucedemo
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://www.saucedemo.com
    
    ${elements}=    Connector.Collect UI Candidates
    Log    \n=== JS_QUERY COLLECTOR (SauceDemo) ===
    Log    Found ${elements.__len__()} elements
    
    Log Many    @{elements}
    
    # Should find at least username, password, and login button
    Should Not Be Empty    ${elements}
    Should Be True    ${elements.__len__()} >= 3
    
    [Teardown]    Close Browser


Test JSQuery Collector Element Details
    [Documentation]    Verify that JSQuery collector captures all required attributes
    [Tags]    collector    js_query    details
    
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
    Should Contain    ${first_element}    clickable
    Should Contain    ${first_element}    enabled
    
    Log    \n=== First Element Details ===
    Log    ${first_element}
    
    [Teardown]    Close Browser


Test JSQuery With BBox Visualization
    [Documentation]    Visualize bounding boxes on screenshot with annotations
    [Tags]    collector    js_query    visualization    bbox
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://the-internet.herokuapp.com/login
    
    # Collect elements
    ${elements}=    Connector.Collect UI Candidates
    Log    Found ${elements.__len__()} elements with bounding boxes
    
    # Take screenshot
    ${screenshot}=    Take Screenshot    filename=original.png    fullPage=True
    
    # Draw bounding boxes and embed in log
    ${annotated}=    Draw And Log Elements    ${elements}    ${screenshot}
    
    Log    ✅ Annotated screenshot saved: ${annotated}
    Log    📦 Total elements annotated: ${elements.__len__()}
    
    Should Not Be Empty    ${annotated}
    
    [Teardown]    Close Browser


Test JSQuery BBox On SauceDemo
    [Documentation]    Test BBox visualization on SauceDemo login page
    [Tags]    collector    js_query    visualization    bbox    saucedemo
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://www.saucedemo.com
    
    # Collect elements
    ${elements}=    Connector.Collect UI Candidates
    Log    Found ${elements.__len__()} elements
    
    # Take screenshot and annotate
    ${screenshot}=    Take Screenshot    filename=saucedemo.png    fullPage=True
    ${annotated}=    Draw And Log Elements    ${elements}    ${screenshot}    width=1000
    
    Log    Annotated: ${annotated}
    
    [Teardown]    Close Browser

