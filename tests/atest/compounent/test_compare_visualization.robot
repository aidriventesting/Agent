*** Settings ***
Documentation    Compare JSQuery and AXTree collectors with side-by-side visualization
Library          Browser
Library          Agent.platforms._webconnector.WebConnectorRF    js_query    AS    JSConnector
Library          Agent.platforms._webconnector.WebConnectorRF    axtree    AS    AXConnector
Library          tests/atest/compounent/BBoxVisualizer.py


*** Test Cases ***
Compare JSQuery vs AXTree With Visualization
    [Documentation]    Visual comparison of two collectors on the same page
    [Tags]    collector    comparison    visualization    bbox
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://the-internet.herokuapp.com/login
    
    # Collect with both collectors
    ${js_elements}=    JSConnector.Collect UI Candidates
    ${ax_elements}=    AXConnector.Collect UI Candidates
    
    Log    JSQuery found: ${js_elements.__len__()} elements
    Log    AXTree found: ${ax_elements.__len__()} elements
    
    # Take screenshot
    ${screenshot}=    Take Screenshot    filename=comparison.png    fullPage=True
    
    # Create comparison image
    ${comparison}=    Create Comparison Image
    ...    ${screenshot}
    ...    ${js_elements}
    ...    ${ax_elements}
    ...    JSQuery (${js_elements.__len__()})
    ...    AXTree (${ax_elements.__len__()})
    
    Log    📊 Comparison image created: ${comparison}
    
    # Also create individual annotated versions
    ${js_annotated}=    Draw BBox On Screenshot
    ...    ${screenshot}
    ...    ${js_elements}
    ...    color=red
    
    ${ax_annotated}=    Draw BBox On Screenshot
    ...    ${screenshot}
    ...    ${ax_elements}
    ...    color=blue
    
    Log    🔴 JSQuery only: ${js_annotated}
    Log    🔵 AXTree only: ${ax_annotated}
    
    [Teardown]    Close Browser


Compare On Complex Page
    [Documentation]    Compare collectors on a more complex page (SauceDemo)
    [Tags]    collector    comparison    visualization    bbox    complex
    
    New Browser    chromium    headless=False
    New Context
    New Page    https://www.saucedemo.com
    
    # Collect with both collectors
    ${js_elements}=    JSConnector.Collect UI Candidates
    ${ax_elements}=    AXConnector.Collect UI Candidates
    
    Log    📊 JSQuery: ${js_elements.__len__()} elements
    Log    📊 AXTree: ${ax_elements.__len__()} elements
    
    ${diff}=    Evaluate    ${js_elements.__len__()} - ${ax_elements.__len__()}
    Log    📊 Difference: ${diff} elements
    
    # Take screenshot and create comparison
    ${screenshot}=    Take Screenshot    filename=saucedemo_compare.png    fullPage=True
    ${comparison}=    Create Comparison Image
    ...    ${screenshot}
    ...    ${js_elements}
    ...    ${ax_elements}
    ...    JSQuery
    ...    AXTree
    
    Log    Comparison saved: ${comparison}
    
    [Teardown]    Close Browser

