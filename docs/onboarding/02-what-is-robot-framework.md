# What is Robot Framework?

Robot Framework (RF) is an open-source, keyword-driven test automation framework.

You write tests in a readable format using keywords (reusable actions), and RF executes them via libraries written in Python/Java/etc.

## Why RF is widely used in QA

- **Readable syntax**: tests look like structured instructions.
- **Easy to extend**: custom keywords can be added in Python.
- **Large ecosystem**: Selenium, Appium, API testing, databases, etc.
- **Good reporting**: logs, screenshots, and HTML reports.

## Core concepts

- **Test case**: a sequence of keywords.
- **Keyword**: an action or verification step.
- **Library**: a collection of keywords (e.g., AppiumLibrary, SeleniumLibrary).
- **Variables**: configs and data for tests.
- **Listener**: a hook system to observe/modify runtime behavior.

## Example test

```robot
*** Test Cases ***
User can login
    Open App
    Type Text    id=username    alice
    Type Text    id=password    secret
    Click        text=Login
    Page Should Contain    Welcome
```

## Why we build the AI agent on top of RF

RF already handles:

- test organization
- environment variables
- reporting
- device/browser integration (via Appium/Selenium)
- CI compatibility

Our agent adds intelligence inside RF rather than reinventing a full framework.

