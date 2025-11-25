*** Settings ***
Documentation    Configuration centralisée pour les tests web
Variables    ${EXECDIR}/tests/atest/browsers/settings.yaml
Library    Browser
Library    Agent    llm_client=openai    llm_model=gpt-4o-mini
*** Keywords ***
Open Website
    [Documentation]    Ouvre le navigateur selon la configuration. Optionnellement navigue vers une URL.
    ...                Args: url (optionnel) - URL vers laquelle naviguer. Si vide, ouvre seulement le navigateur.
    [Arguments]    ${url}=${EMPTY}
    New Browser    ${browser_type}    headless=${headless_mode}
    Log    Browser opened - Type: ${browser_type}, Headless: ${headless_mode}
    New Page    ${url}
    