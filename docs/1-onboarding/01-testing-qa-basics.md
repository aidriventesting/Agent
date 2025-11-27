# Testing & QA basics (quick context)

> **Note**: This document focuses on **test automation** as the primary use case. However, the challenges and principles described here also apply to web scraping and general workflow automation. We use testing as a detailed example because it's the most common and well-documented automation scenario.

## Why test software?

Software changes constantly. Every new feature, bug fix, or refactor can break existing functionality.

Imagine you're building an app:

**Sprint 1**: You ship login. You test it manually. ✓ Works. **5 minutes.**

**Sprint 2**: You add a dashboard. You test the dashboard, but also need to verify login still works (regression testing). **10 minutes.**

**Sprint 5**: You have 20 features. Each new PR requires testing the new feature + verifying the 20 existing ones. **2 hours per PR.**

**Month 6**: You have 50 features. **5+ hours per PR.**

**Year 1**: You have 100 features with 1000 acceptance criteria. Manual testing becomes impossible. **Days per release.**

### The compound problem

The pain isn't just volume:

- **Frequent merges**: Teams merge code multiple times per day. Testing 100+ scenarios manually each time? Impossible.

- **Features evolve**: Login changes from username to email. Every scenario depending on login must be updated and retested.

- **Criteria change**: "User sees welcome message" becomes "User sees personalized dashboard with real-time metrics". Old test scenarios need maintenance.

- **Multiple platforms**: Web + Android + iOS = 3× the effort.

Without automation, you face impossible choices:
1. **Skip regression tests** → Bugs slip through to production
2. **Slow down releases** → Wait days for manual QA cycles
3. **Hire a huge QA team** → Expensive and doesn't scale

**Automation solves this**: Write a test once, run it thousands of times. Tests become code that validates your code.

## Types of automated tests

Not all tests are created equal. They differ in speed, cost, and what they validate.

### Unit tests
Verify small pieces of code in isolation (a function, a class method).

- **Fast**: Milliseconds per test
- **Cheap**: Easy to write and maintain
- **Stable**: No external dependencies
- **Limitation**: Don't catch integration issues

### API / Integration tests
Validate services, contracts, and how components work together.

- **Medium speed**: Seconds per test
- **Medium cost**: Require test data and environment setup
- **Stable**: More reliable than UI tests
- **Limitation**: Don't catch UI bugs

### End-to-end (E2E) tests
Simulate real user flows through the UI. Click buttons, fill forms, navigate screens.

- **Slow**: Seconds to minutes per test
- **Expensive**: Hard to write and maintain
- **Brittle**: Break often for non-bug reasons
- **Highest value**: Catch real user-facing issues

**A healthy test strategy**: Many unit tests + medium API tests + smaller set of critical E2E tests.

We focus on E2E tests because they're the most painful to maintain, yet essential for catching real bugs and ONLY E2E GIVE CONFIDENCE TO SHIP THE BUILD.

## Why E2E tests are hard

E2E automation interacts with the UI, which is inherently unstable:

- **Dynamic**: Async loading, animations, API calls
- **Redesigned frequently**: UI changes every sprint
- **Platform differences**: Same feature, different UI on web/Android/iOS
- **Data dependent**: Tests fail when data changes
- **Environment specific**: Staging vs production behave differently

So E2E tests often fail because of:

- **Timing issues**: "Element not ready yet" even though the app works
- **Locator brittleness**: Developer changes `id="submit-btn"` to `id="submit-button"`, test breaks
- **Minor UI shifts**: Button moved 10px left, XPath locator fails
- **Non-deterministic data**: "5 new messages" changes to "3 new messages"

These failures aren't bugs — they're maintenance overhead. Teams spend more time fixing tests than writing them.

## Important terms

Before diving deeper, here are key concepts used throughout the docs:

- **Test case**: One scenario to validate (e.g., "User can login with valid credentials").
- **Test suite**: Collection of related test cases (e.g., "Login suite" with 10 test cases).
- **Regression testing**: Rerunning tests to ensure old features still work after changes.
- **Smoke test**: Small suite validating basic health (e.g., "Can the app start?").
- **Locator / selector**: How automation finds a UI element (`id=username`, `text=Login`, `xpath=//button[3]`).
- **Assertion / check**: Expected outcome to verify (`page should contain "Welcome"`, `button should be clickable`).
- **Flakiness**: Intermittent test failures not caused by real bugs. The test passes when rerun without code changes.

## What good automation looks like

Despite the challenges, well-designed E2E automation is valuable:

- **Stable and reproducible**: Passes consistently when the app works, fails consistently when broken.
- **Clear failures**: Provides logs, screenshots, and exact error messages.
- **Minimal brittle selectors**: Uses stable identifiers, not fragile XPath based on position.
- **Focused on value**: Tests high-impact user journeys, not every edge case.
- **Fast enough**: Provides feedback in minutes, not hours.

Traditional automation struggles to achieve this. That's where our AI agent comes in.

## Summary: The testing challenge

We need E2E tests to catch real bugs, but they're expensive to maintain:

- **Volume**: 100+ features × 3 platforms = hundreds of scenarios
- **Evolution**: Features and criteria change constantly
- **Instability**: UI changes, timing issues, brittle locators
- **Maintenance**: More time fixing tests than writing them

Our project aims to keep the value of E2E tests while dramatically reducing the maintenance cost through AI-driven automation.

In the next docs, you'll see in more details how traditional automation works, why it's still painful even with good tools, and how the agent solves these problems.
