*** Settings ***
Documentation    Quick smoke test to verify collector system works
Library          Agent.platforms._webconnector.WebConnectorRF    js_query    AS    JSQueryConn
Library          Agent.platforms._webconnector.WebConnectorRF    axtree    AS    AXTreeConn


*** Test Cases ***
Verify JSQuery Connector Works
    [Documentation]    Test that JSQuery connector can be instantiated
    [Tags]    smoke    js_query
    
    ${strategy}=    Get Variable Value    ${JSQueryConn.collector_strategy}
    Should Be Equal    ${strategy}    js_query
    Log To Console    \n✓ JSQuery connector created with strategy: ${strategy}


Verify AXTree Connector Works
    [Documentation]    Test that AXTree connector can be instantiated
    [Tags]    smoke    axtree
    
    ${strategy}=    Get Variable Value    ${AXTreeConn.collector_strategy}
    Should Be Equal    ${strategy}    axtree
    Log To Console    ✓ AXTree connector created with strategy: ${strategy}


Verify Different Collectors Are Independent
    [Documentation]    Test that two connectors with different strategies are separate instances
    [Tags]    smoke
    
    ${js_strategy}=    Get Variable Value    ${JSQueryConn.collector_strategy}
    ${ax_strategy}=    Get Variable Value    ${AXTreeConn.collector_strategy}
    
    Should Be Equal    ${js_strategy}    js_query
    Should Be Equal    ${ax_strategy}    axtree
    Should Not Be Equal    ${js_strategy}    ${ax_strategy}
    
    Log To Console    \n✓ Multiple independent collectors work correctly

