*** Settings ***
Documentation    Tests for Agent.Find Visual Element keyword
Resource    ../browsers/config.robot
Test Setup    Open Website    https://agent-arena-eta.vercel.app/snapshots/v1/arena/search/c2/
Test Teardown    Close Browser

*** Test Cases ***
Find Element Center Coordinates
    [Documentation]    Find element and get center coordinates (default)
    ${coords}=    Agent.Find Visual Element    input search element
    Log    Center coordinates: ${coords}
    Should Contain    ${coords}    x
    Should Contain    ${coords}    y

Find Element Pixel BBox
    [Documentation]    Find element and get pixel bounding box
    ${bbox}=    Agent.Find Visual Element    search botton    format=pixels
    Log    Pixel bbox: ${bbox}
    Should Contain    ${bbox}    x1
    Should Contain    ${bbox}    y1
    Should Contain    ${bbox}    x2
    Should Contain    ${bbox}    y2
