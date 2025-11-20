# Why this project exists

Modern products ship fast. UI changes constantly. End-to-end (E2E) tests are essential to catch real user bugs, but they're expensive to write and painful to maintain.

This project builds an AI-driven testing agent that can interact with mobile or web apps the way a human tester does:

- perform actions on the UI (tap, type, scroll, click)
- verify what it sees on screen
- help create and maintain tests with less manual effort

## The problem we're solving

Today, E2E automation suffers from:

- **High authoring cost**: writing and updating long UI scripts takes time.
- **Flakiness**: tests fail for reasons unrelated to product bugs (timing, unstable locators, minor UI changes).
- **Locator brittleness**: UI identifiers change often.
- **Visual-only elements**: maps, canvas views, images, or custom widgets are hard to validate with classic locators.
- **Slow feedback loops**: regressions are detected late.

## What we aim for

- Reduce time to automate UI flows.
- Make test maintenance cheaper through self-healing and visual checks.
- Let testers express intent in higher-level terms (not low-level selectors).
- Provide deterministic logs and reports for debugging.

## What we are not building (yet)

- A general-purpose autonomous agent for all apps.
- A replacement for unit/API tests.
- A system that runs without evaluation or control.
- Magic "zero-maintenance tests." We aim for **less maintenance**, not **none**.

