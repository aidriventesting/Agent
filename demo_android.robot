*** Settings ***
Documentation    Demo: AI-driven Android test with Robot Framework Agent
...              Standalone file - just update the variables below and run
Library    AppiumLibrary
Library    Agent    llm_client=openai    llm_model=gpt-4.1    platform_type=mobile    element_source=accessibility


*** Variables ***
# Appium server
${APPIUM_URL}              http://127.0.0.1:4723

# Device config
${DEVICE_NAME}             YOUR_DEVICE_NAME
${PLATFORM_NAME}           Android
${AUTOMATION_NAME}         UiAutomator2

# App config (choose one)
${APP_PACKAGE}             com.google.android.youtube
${APP_ACTIVITY}            .app.honeycomb.Shell$HomeActivity


*** Test Cases ***
Demo Youtube
    [Documentation]    Demo Youtube
    Open Demo App

    Agent.check    instruction=Verify that YouTube watch history is turned off

    Agent.Do       instruction=Tap the search icon at the top

    Agent.Do       instruction=Enter "Robot Framework" into the search input box

    Agent.check    instruction=Confirm every result displayed includes "Robot Framework" in its title or description

    Agent.Do       instruction=Click on the first search result appearing in the search results list

    Agent.Ask      question=How many subscribers does the Robot Framework channel have?




*** Keywords ***
Open Demo App
    [Documentation]    Opens the configured Android app
    Open Application    
    ...    remote_url=${APPIUM_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    appium:deviceName=${DEVICE_NAME}
    ...    appium:automationName=${AUTOMATION_NAME}
    ...    appium:appPackage=${APP_PACKAGE}
    ...    appium:appActivity=${APP_ACTIVITY}
    ...    appium:noReset=${TRUE}

