# Why an agentic AI for testing?

Classic automation is powerful but rigid: it executes exactly what you coded.

An agentic AI adds reasoning and flexibility:

- It understands test intent.
- It observes the UI.
- It decides and performs actions.
- It verifies outcomes visually or structurally.
- It can recover from unexpected UI changes.

## What "agentic" means here

Not sci-fi autonomy. Practically, it means:

- a loop of **observe → act → check**
- bounded by tools and rules
- producing deterministic artifacts for debugging

## What problems this approach helps with

### Faster test creation

Write intent, not low-level scripts.

### Self-healing

If one locator breaks, the agent can find alternatives.

### Visual validation

Screens with images/widgets are testable.

### Lower flakiness

The agent can wait, retry, or replan based on state.

### Better failure diagnosis

Rich reasoning + screenshots + structured logs.

## Scope of V1

V1 focuses on two primitives:

- **Agent.Do**: perform a single UI action.
- **Agent.Check**: verify the UI state using visual reasoning.

Planning, memory, and full autonomy come later.

