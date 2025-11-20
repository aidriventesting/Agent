# Testing & QA basics (quick context)

## Types of tests

- **Unit tests**: verify small pieces of code in isolation. Fast, cheap, stable.
- **API / integration tests**: validate services and contracts. Medium cost, stable.
- **End-to-end (E2E) tests**: simulate real user flows through the UI. Slowest and most brittle, but highest real-world confidence.

A healthy system uses many unit/API tests + a smaller set of E2E tests.

## Why E2E tests are hard

E2E automation interacts with the UI, which is:

- dynamic (async loading, animations)
- frequently redesigned
- different across devices/browsers
- dependent on data and environment

So E2E tests often fail because of:

- timing issues ("element not ready yet")
- unstable identifiers
- minor UI shifts
- non-deterministic data

## Important terms

- **Test case**: one scenario to validate.
- **Test suite**: collection of test cases.
- **Regression**: rerunning tests to ensure old features still work.
- **Smoke test**: small suite to validate basic health.
- **Locator / selector**: how automation finds a UI element (id, text, xpath, etc.).
- **Assertion / check**: the expected outcome (something should exist, text should match, etc.).
- **Flakiness**: intermittent failures not representing real bugs.

## What good automation looks like

- Stable and reproducible.
- Clear failures with logs and screenshots.
- Minimal brittle selectors.
- Focused on high-value user journeys.

