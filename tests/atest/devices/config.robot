*** Settings ***
Documentation    Configuration centralisée pour Local et BrowserStack
Variables    ${EXECDIR}/tests/atest/devices/settings.yaml
Library    AppiumLibrary

*** Keywords ***
Open Application With Config
    [Documentation]    Ouvre l'application selon Device_location dans settings.yaml
    ...                Options: Local ou Browserstack
    Run Keyword If    '${Device_location}' == 'Local'    Open Local Application
    ...    ELSE IF    '${Device_location}' == 'Browserstack'    Open BrowserStack Application
    ...    ELSE    Fail    Device_location invalide: ${Device_location}

Open Local Application
    [Documentation]    Ouvre l'application avec configuration locale
    Import Resource    ${EXECDIR}/tests/atest/devices/_local.robot
    Run Keyword If    '${platformName}' == 'Android'    Open Application    remote_url=${remote_url}    &{DESIRED_CAPABILITIES_Android}
    ...    ELSE IF    '${platformName}' == 'iOS'    Open Application    remote_url=${remote_url}    &{DESIRED_CAPABILITIES_iOS}
    ...    ELSE    Fail    platformName invalide: ${platformName}
    Log    Application locale ouverte - Platform: ${platformName}

Open BrowserStack Application
    [Documentation]    Ouvre l'application avec configuration BrowserStack (via BrowserStack SDK)
    Import Variables    ${EXECDIR}/browserstack.yml
    Import Resource    ${EXECDIR}/tests/atest/devices/_browserstack.robot
    # BrowserStack SDK gère automatiquement les capabilities depuis browserstack.yml
    Open Application    remote_url=${remote_url}
    Log    Application BrowserStack ouverte

