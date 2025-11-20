# Traditional automation problems

Even with great tools like Selenium and Appium, E2E automation is expensive to maintain. This doc explains why.

## How traditional automation works: Locators

Traditional automation relies on **locators** — identifiers that tell the tool which UI element to interact with.

### Locators on Web

Web pages are built with HTML. Every element has properties you can target:

```html
<button id="login-btn" class="primary">Login</button>
<input type="text" name="username" placeholder="Enter your email">
```

**Common web locators**:
- **ID**: `id=login-btn` (best when available)
- **CSS selector**: `.primary` or `button.primary`
- **XPath**: `//button[text()='Login']` (powerful but fragile)
- **Text**: `text=Login`
- **Name**: `name=username`

### Locators on Mobile

Mobile apps have a view hierarchy. Each element has properties:

```xml
<Button 
  resource-id="com.example:id/login" 
  text="Login" 
  content-desc="Login button"/>
<TextField 
  resource-id="com.example:id/username" 
  hint="Enter username"/>
```

**Common mobile locators**:
- **Resource ID**: `id=com.example:id/login` (Android)
- **Accessibility ID**: `accessibility id=Login button` (iOS/Android)
- **XPath**: `//android.widget.Button[@text='Login']`
- **Text**: `text=Login`

### Key difference: Web vs Mobile

**Web**: More stable IDs and CSS selectors. Developers often add meaningful IDs.

**Mobile**: IDs are less common. Many elements lack `resource-id` or `content-desc`, forcing fragile XPath locators based on position.

## Before Robot Framework: Raw automation code

Here's a very basic Selenium test in Python:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_user_login():
    # Setup driver
    driver = webdriver.Chrome()
    driver.get("https://example.com/login")
    
    try:
        # Wait for username field
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.send_keys("alice@example.com")
        
        # Find and fill password
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("secret123")
        
        # Click login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()
        
        # Wait and verify success
        time.sleep(2)
        welcome_text = driver.find_element(By.CSS_SELECTOR, ".welcome-message")
        assert "Welcome" in welcome_text.text
        
    finally:
        driver.quit()
```

**Problems**:
- **Verbose**: 30+ lines for a simple login test
- **Technical**: Requires programming knowledge (imports, waits, exception handling)
- **Fragile**: If `id="username"` changes to `id="email"`, test breaks
- **Hard to maintain**: Changing one locator means editing code

### The real problem: scaling to 100+ tests

This example is **basic**. In reality, when you have 100+ tests, the complexity explodes:

- **Design patterns needed**: Page Object Model, Factory patterns, Builder patterns to organize code
- **Strong programming skills required**: Object-oriented programming, inheritance, abstraction
- **Infrastructure code**: Test data management, configuration handling, reporting hooks, retry mechanisms
- **Code review overhead**: Every test change requires reviewing complex Python/Java code
- **High entry barrier**: Junior QA engineers can't contribute without solid programming background

**Result**: E2E automation becomes a software engineering project itself. You need senior developers just to write and maintain tests.

## With Robot Framework: Better but still hard

Robot Framework makes tests more readable:

```robot
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
User Can Login
    Open Browser    https://example.com/login    chrome
    Input Text      id=username    alice@example.com
    Input Text      id=password    secret123
    Click Button    xpath=//button[@type='submit']
    Wait Until Page Contains    Welcome
    Close Browser
```

**Better because**:
- Much more readable
- QA without deep programming can write/read tests
- Reusable keywords hide complexity
- Easy to organize suites and variables

**Still has problems**:
- You still write locators manually
- When UI changes, you manually update locators
- No visual understanding
- At 100+ tests: still need design patterns, DRY principle, Single Responsibility, good architecture --> Still somehow costly to write and to maintain

## The 8 core problems

### 1. Brittle locators

**Problem**: Developer changes `id=submit-button` to `id=submit-btn`.

```robot
Click Button    id=submit-button  # ❌ Breaks
```

**Cost**: You manually find the new locator and update all tests using it.

### 2. Dynamic content

**Problem**: Dashboard shows "5 new messages" but the number changes based on data.

```robot
Page Should Contain    5 new messages  # ❌ Fails when count is different
```

**Cost**: Tests become data-dependent. Valid builds fail.

### 3. Timing and async loading

**Problem**: Button appears after an API call, but test clicks too early.

```robot
Click Button    id=load-more  # ❌ Fails if button not ready
```

**Cost**: You add `Sleep 3s`, making tests slow and still flaky.

### 4. Environment-specific data

**Problem**: Production shows "John Doe", staging shows "Test User".

```robot
Page Should Contain    John Doe  # ❌ Fails in staging
```

**Cost**: Separate tests per environment or complex variable management.

### 5. Cross-platform locator differences

**Problem**: Same button, different locators per platform.

- Web: `id=menu`
- Android: `resource-id=com.app:id/menu`
- iOS: `accessibility id=Menu`

```robot
Click Element    id=menu  # ❌ Only works on web
```

**Cost**: Write and maintain separate tests for each platform.

### 6. Visual elements can't be validated

**Problem**: App shows a map, chart, or image. Locators can't verify content.

```robot
Page Should Contain Element    id=map  # ✓ Map exists
# ❌ But is the map showing the right data?
```

**Cost**: Visual bugs slip through. Manual testing still needed.

### 7. Accessibility issues on mobile

**Problem**: Button has no `content-desc` or `resource-id`. Only way to find it is fragile XPath.

```robot
Click Element    xpath=//android.widget.Button[3]  # ❌ Breaks on layout change
```

**Cost**: Tests break on minor UI rearrangements.

### 8. Complex debugging

**Problem**: Test fails at step 15 of a 20-step flow. You only get "Element not found".

**Cost**: You rerun the flow repeatedly, adding print statements, until you find the issue.

## Why this matters

Each problem seems small, but they compound:

- A test suite with 100 tests
- Each test has ~10 locators
- UI changes once per sprint
- = 1000 locators to potentially maintain
- = Hours of weekly maintenance

**Result**: Teams write fewer E2E tests or let them rot.

## What's next

In the following docs, we'll see:
- What Robot Framework provides (doc 04)
- How AI agents solve these problems (doc 05)

