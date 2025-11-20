# Automation tools explained

If you're new to test automation, you might wonder: what are Selenium, Appium, and Playwright? Why do we need them?

This doc explains the main automation frameworks and why our AI agent builds on top of them.

## The three main automation tools

### Selenium (Web automation)

**What it is**: The most popular open-source tool for automating web browsers.

**What it does**: Opens browsers (Chrome, Firefox, Safari), clicks buttons, fills forms, navigates pages, reads page content.

**Why it's widely used**:
- Mature and battle-tested
- Supports all major browsers
- Works across languages (Python, Java, JavaScript, C#, etc.)
- Large community and ecosystem

**Example use case**: Testing a web app's login flow by opening Chrome, filling username/password, clicking submit, and verifying the dashboard loads.

### Appium (Mobile automation)

**What it is**: An extension of Selenium's approach for mobile apps (Android and iOS).

**What it does**: Controls native, hybrid, and mobile web apps. Taps buttons, types text, swipes, scrolls, reads screen elements on real devices or emulators.

**Why it's widely used**:
- Cross-platform (one tool for Android + iOS)
- Open-source
- Uses the same WebDriver protocol as Selenium
- Works with real devices and emulators

**Example use case**: Testing a shopping app by launching it on an Android device, adding items to cart, and completing checkout.

### Playwright (Modern web automation)

**What it is**: A newer tool from Microsoft for web automation, designed for modern JavaScript-heavy apps.

**What it does**: Similar to Selenium but with better handling of single-page apps (React, Vue, Angular), automatic waiting, and built-in features for screenshots and network interception.

**Why it's gaining popularity**:
- Less flaky than Selenium
- Faster execution
- Better developer experience
- Great for headless testing (no visible browser)
- Built-in handling of modern web patterns

**Example use case**: Testing a React dashboard that loads data asynchronously, with automatic waiting for elements and network requests.

## Why should AI-driven tests use these tools?

These tools already solve the hard infrastructure problems:

### 1. Device and browser control
They know how to start apps, launch browsers, and handle different operating systems.

### 2. Element inspection
They provide access to the UI structure:
- **Web**: DOM (Document Object Model)
- **Mobile**: View hierarchy ( Which is based on accessibility )

### 3. Cross-platform support
Write tests that can run on different browsers (Chrome, Firefox, Safari) or devices (Android, iOS).

### 4. Battle-tested stability
These tools are used by thousands of companies in production. They handle edge cases, browser versions, and platform differences.

### 5. Rich ecosystems
Extensions, integrations, and community support for CI/CD, reporting, and debugging.

## What our AI agent adds

Our agent doesn't replace Selenium/Appium/Playwright — it makes them smarter.

**What these tools provide**:
- "How to tap a button on Android"
- "How to fill a text field in Chrome"
- "How to scroll on iOS"

**What our agent adds**:
- "Which button should I tap?"
- "Is this the right screen?"
- "What should I do if the expected element isn't there?"

The agent brings reasoning, visual understanding, and adaptability on top of the solid infrastructure these tools provide.

## Summary

| Tool | Purpose | Platforms |
|------|---------|-----------|
| **Selenium** | Web automation | Chrome, Firefox, Safari, Edge |
| **Appium** | Mobile automation | Android, iOS (native + hybrid) |
| **Playwright** | Modern web automation | Chrome, Firefox, Safari (WebKit) |

In the next docs, we'll see why traditional automation with these tools is still hard, and how our AI agent solves those problems.

