# Robot Framework Agent

Enable Agent-mode automation. Write natural-language steps; and let the Agent turns them into tool-based UI actions and checks on web and mobile.

[![RoboCon 2026 – What if Robot Framework Had a Brain](https://img.shields.io/badge/RoboCon%202026-What%20if%20Robot%20Framework%20Had%20a%20Brain-orange?style=for-the-badge)](https://www.robocon.io/agenda/helsinki#what-if-robot-framework-have-a-brain)

Alpha — An evolving experiment, with varying levels of maturity across keywords - Not recommended for production yet.

## Quick Start

```robot
*** Settings ***
Library    Agent    llm_client=openai    llm_model=gpt-4o-mini

*** Test Cases ***
Login
    Agent.Do        enter "user@example.com" in email field
    Agent.Do        enter "password1234" in the password field
    Agent.Do        click on login button
    Agent.Check     verify homepage is displayed
```

## Installation

```bash
# Core
pip install robotframework-agent

# Web testing (+ Playwright)
pip install robotframework-agent[web]

# Mobile testing (+ Appium)
pip install robotframework-agent[mobile]

# Development (all tools)
pip install robotframework-agent[dev]
```

## Keywords

**Agent.Do** `<instruction>`
- Execute actions: click, scroll, input text, select, navigate
- Example: `Agent.Do    scroll down to footer`

**Agent.Check** `<instruction>`
- Perform a visual or semantic verification.
- Example: `Agent.Check    verify login form is visible`

**Agent.Ask** `<question>` `format=text|json`
- Query current UI state
- Example: `Agent.Ask    What is the product price?`

**Agent.Find Visual Element** `<description>` `format=normalized|pixels|center`
- Locate elements by description
- Example: `Agent.Find Visual Element    search button`

## Technical Notes

```
Instruction → LLM → UI Context → Tool Selection → Execution
```


Design choices are informed by research on AI agents and UI perception.
Ideas are iterated and evaluated in our evolving lab suite:
[AgentArena](https://github.com/aidriventesting/AgentArena).


## Presented at RoboCon 2026 (Helsinki)

This project will be showcased at RoboCon 2026 during the talk **"What if Robot Framework Had a Brain?"**  
👉 https://www.robocon.io/agenda/helsinki#what-if-robot-framework-have-a-brain


## Contributing

Builders, testers, and curious minds welcome.
Code, issues, and real-world use cases help shape the project.