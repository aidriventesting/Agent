*** Settings ***
Documentation    Web browser configuration
Variables    ${EXECDIR}/tests/atest/config/settings.yaml
Library    Browser
Library    Agent    llm_client=openai    llm_model=gpt-4o

*** Keywords ***
Open Website
    [Documentation]    Opens browser and optionally navigates to URL
    ...                Args: url (optional) - URL to navigate to
    ...                element_source: tree | visual (default: tree)
    ...                selection_mode: text | som (default: text)
    [Arguments]    ${url}=${EMPTY}   ${element_source}=dom    ${selection_mode}=som
    Setup Agent Mode        ${element_source}     ${selection_mode}
    New Browser    ${browser_type}    headless=${headless_mode}    
    New Context    locale=en-US
    Log    Browser opened - Type: ${browser_type}, Headless: ${headless_mode}
    New Page    ${url}
    Set Viewport Size    width=1920    height=1080


Setup Agent Mode
    [Documentation]    Configure Agent element source and selection modes
    [Arguments]    ${element_source}    ${selection_mode}
    ${agent}=    Get Library Instance    Agent
    Call Method    ${agent.engine}    set_element_source    ${element_source}
    Call Method    ${agent.engine}    set_llm_input_format    ${selection_mode}
    Log    Agent configured - element_source: ${element_source}, selection_mode: ${selection_mode}

