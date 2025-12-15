*** Settings ***
Documentation    Compare different collector strategies side-by-side
Library          Browser
Library          Agent.platforms._webconnector.WebConnectorRF    js_query    AS    JSQueryConnector
Library          Agent.platforms._webconnector.WebConnectorRF    axtree    AS    AXTreeConnector
Library          Collections


*** Test Cases ***
Compare Collectors On Simple Login Form
    [Documentation]    Compare JSQuery and AXTree collectors on the same login form
    [Tags]    collector    compare    login
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://the-internet.herokuapp.com/login
    
    # Collect with JSQuery
    ${js_elements}=    JSQueryConnector.Collect UI Candidates
    Log To Console    \n=== COMPARISON: Simple Login Form ===
    Log To Console    JSQuery found: ${js_elements.__len__()} elements
    
    # Collect with AXTree
    ${ax_elements}=    AXTreeConnector.Collect UI Candidates
    Log To Console    AXTree found: ${ax_elements.__len__()} elements
    
    # Compare counts
    ${diff}=    Evaluate    ${js_elements.__len__()} - ${ax_elements.__len__()}
    Log To Console    Difference: ${diff} elements
    
    # Log some details
    Log To Console    \n=== JSQuery First 5 Elements ===
    Log To Console    ${js_elements[:5]}
    
    Log To Console    \n=== AXTree First 5 Elements ===
    Log To Console    ${ax_elements[:5]}
    
    Should Not Be Empty    ${js_elements}
    Should Not Be Empty    ${ax_elements}
    
    [Teardown]    Close Browser


Compare Collectors On SauceDemo
    [Documentation]    Compare collectors on SauceDemo login page
    [Tags]    collector    compare    saucedemo
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://www.saucedemo.com
    
    # Collect with JSQuery
    ${js_elements}=    JSQueryConnector.Collect UI Candidates
    Log To Console    \n=== COMPARISON: SauceDemo ===
    Log To Console    JSQuery found: ${js_elements.__len__()} elements
    
    # Collect with AXTree
    ${ax_elements}=    AXTreeConnector.Collect UI Candidates
    Log To Console    AXTree found: ${ax_elements.__len__()} elements
    
    # Compare counts
    ${diff}=    Evaluate    ${js_elements.__len__()} - ${ax_elements.__len__()}
    Log To Console    Difference: ${diff} elements
    
    # Analyze element types
    ${js_inputs}=    Count Element Type    ${js_elements}    input
    ${ax_inputs}=    Count Element Type    ${ax_elements}    input
    Log To Console    \nInput fields - JSQuery: ${js_inputs}, AXTree: ${ax_inputs}
    
    ${js_buttons}=    Count Element Type    ${js_elements}    button
    ${ax_buttons}=    Count Element Type    ${ax_elements}    button
    Log To Console    Buttons - JSQuery: ${js_buttons}, AXTree: ${ax_buttons}
    
    ${js_links}=    Count Element Type    ${js_elements}    a
    ${ax_links}=    Count Element Type    ${ax_elements}    a
    Log To Console    Links - JSQuery: ${js_links}, AXTree: ${ax_links}
    
    [Teardown]    Close Browser


Compare Collectors On React SPA
    [Documentation]    Compare collectors on a React single-page application
    [Tags]    collector    compare    spa
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://react-shopping-cart-67954.firebaseapp.com/
    
    # Collect with JSQuery
    ${js_elements}=    JSQueryConnector.Collect UI Candidates
    Log To Console    \n=== COMPARISON: React Shopping Cart SPA ===
    Log To Console    JSQuery found: ${js_elements.__len__()} elements
    
    # Collect with AXTree
    ${ax_elements}=    AXTreeConnector.Collect UI Candidates
    Log To Console    AXTree found: ${ax_elements.__len__()} elements
    
    # Compare counts
    ${diff}=    Evaluate    ${js_elements.__len__()} - ${ax_elements.__len__()}
    Log To Console    Difference: ${diff} elements
    
    # Log element samples
    Log To Console    \n=== JSQuery Sample (first 3) ===
    FOR    ${element}    IN    @{js_elements[:3]}
        Log To Console    - ${element['class_name']}: ${element['text'][:50]} | role: ${element['role']}
    END
    
    Log To Console    \n=== AXTree Sample (first 3) ===
    FOR    ${element}    IN    @{ax_elements[:3]}
        Log To Console    - ${element['class_name']}: ${element['text'][:50]} | role: ${element['role']}
    END
    
    Should Not Be Empty    ${js_elements}
    Should Not Be Empty    ${ax_elements}
    
    [Teardown]    Close Browser


*** Keywords ***
Count Element Type
    [Documentation]    Count how many elements of a specific tag type are in the list
    [Arguments]    ${elements}    ${tag_name}
    
    ${count}=    Set Variable    0
    FOR    ${element}    IN    @{elements}
        ${class_name}=    Get From Dictionary    ${element}    class_name
        ${count}=    Run Keyword If    '${class_name}' == '${tag_name}'
        ...    Evaluate    ${count} + 1
        ...    ELSE    Set Variable    ${count}
    END
    
    RETURN    ${count}

