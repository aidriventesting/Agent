*** Settings ***
Documentation    Mobile device configuration for Local and BrowserStack
Variables    ${EXECDIR}/tests/atest/config/settings.yaml
Library    AppiumLibrary
Library    Agent    llm_client=openai    llm_model=gpt-4o   platform_type=mobile

*** Keywords ***
Open Application With Config
    [Documentation]    Opens application based on Device_location setting
    ...                Options: Local or Browserstack
    ...                element_source: tree | visual (default: tree)
    [Arguments]    ${element_source}=dom    ${selection_mode}=som
    Setup Agent Mode    ${element_source}    ${selection_mode}
    Run Keyword If    '${Device_location}' == 'Local'    Open Local Application
    ...    ELSE IF    '${Device_location}' == 'Browserstack'    Open BrowserStack Application
    ...    ELSE    Fail    Device_location invalid: ${Device_location}

Open Local Application
    [Documentation]    Opens application with local configuration
    Import Resource    ${EXECDIR}/tests/atest/config/_local.robot
    Run Keyword If    '${platformName}' == 'Android'    Open Application    remote_url=${remote_url}    &{DESIRED_CAPABILITIES_Android}
    ...    ELSE IF    '${platformName}' == 'iOS'    Open Application    remote_url=${remote_url}    &{DESIRED_CAPABILITIES_iOS}
    ...    ELSE    Fail    platformName invalid: ${platformName}
    Log    Local application opened - Platform: ${platformName}

Open BrowserStack Application
    [Documentation]    Opens application with BrowserStack configuration
    
    Import Variables    ${EXECDIR}/browserstack.yml
    Import Resource    ${EXECDIR}/tests/atest/config/_browserstack.robot
    Open Application    remote_url=${remote_url}
    Log    BrowserStack application opened

Setup Agent Mode
    [Documentation]    Configure Agent element source and selection modes
    [Arguments]    ${element_source}    ${selection_mode}
    ${agent}=    Get Library Instance    Agent
    Call Method    ${agent.engine}    set_element_source    ${element_source}
    Call Method    ${agent.engine}    set_llm_input_format    ${selection_mode}
    Log    Agent configured - element_source: ${element_source}, selection_mode: ${selection_mode}


