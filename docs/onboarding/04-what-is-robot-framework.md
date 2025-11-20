# What is Robot Framework?

Robot Framework (RF) is an open-source, keyword-driven test automation framework.

You write tests in a readable format using keywords (reusable actions), and RF executes them via libraries written in Python/Java/etc.

## Why RF is widely used in QA

- **Readable syntax**: Tests look like structured instructions, not code.
- **Easy to extend**: Add custom keywords in Python.
- **Large ecosystem**: Selenium, Appium, API testing, databases, SSH, etc.
- **Good reporting**: Logs, screenshots, and HTML reports out of the box.
- **Cross-platform**: Works on Windows, Mac, Linux.

## Core concepts

### Test case
A sequence of keywords that validates one scenario.

### Keyword
An action or verification step. Can be built-in or custom.

### Library
A collection of keywords. Examples:
- `SeleniumLibrary` - web automation
- `AppiumLibrary` - mobile automation
- `RequestsLibrary` - API testing
- `DatabaseLibrary` - SQL queries

### Variables
Store configs and test data:

```robot
*** Variables ***
${USERNAME}    alice@example.com
${PASSWORD}    secret123
${BASE_URL}    https://example.com
```

### Listener
A hook system to observe or modify test execution at runtime. Our AI agent uses listeners to intercept steps.

## Example test

```robot
*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}        https://example.com
${BROWSER}    chrome

*** Test Cases ***
User Can Login
    Open Browser    ${URL}/login    ${BROWSER}
    Input Text      id=username     alice@example.com
    Input Text      id=password     secret123
    Click Button    text=Login
    Wait Until Page Contains    Welcome
    Close Browser

User Cannot Login With Wrong Password
    Open Browser    ${URL}/login    ${BROWSER}
    Input Text      id=username     alice@example.com
    Input Text      id=password     wrong
    Click Button    text=Login
    Page Should Contain    Invalid credentials
    Close Browser
```

## Structure of a Robot test file

```robot
*** Settings ***
# Libraries, resources, and setup/teardown
Library           SeleniumLibrary
Suite Setup       Open Browser    ${URL}    chrome
Suite Teardown    Close Browser

*** Variables ***
# Test data and configs
${URL}    https://example.com

*** Test Cases ***
# Your test scenarios
My Test Case
    Log    This is a test
    Should Be Equal    2    2

*** Keywords ***
# Custom reusable keywords
Login As User
    [Arguments]    ${username}    ${password}
    Input Text     id=username    ${username}
    Input Text     id=password    ${password}
    Click Button   text=Login
```

## Why we build the AI agent on top of RF

RF already handles the hard parts:

### 1. Test organization
Suites, test cases, tags, setup/teardown.

### 2. Environment variables
Easy config management across environments.

### 3. Reporting
HTML logs with screenshots, timing, and pass/fail status.

### 4. Device/browser integration
Via Appium and Selenium libraries.

### 5. CI compatibility
Runs in Jenkins, GitHub Actions, GitLab CI, etc.

### 6. Extensibility
We add our AI keywords (`Agent.Do`, `Agent.Check`) as a Python library.

### 7. Listener system
We hook into RF's execution to observe steps and inject reasoning.

## Our approach

Instead of reinventing a test framework, we:

1. Use RF's structure and reporting
2. Add AI-powered keywords as a library
3. Let RF handle execution, variables, and artifacts
4. Focus on making the keywords intelligent

**Result**: Teams keep their existing RF knowledge and infrastructure, but get smarter tests.

## What RF doesn't solve (and we do)

RF still requires:
- Manual locators
- Hardcoded waits
- Brittle selectors
- No visual validation

That's where our agent comes in (see next doc).

