# Robot Framework Agent

Enable Agent-mode automation. Write natural-language steps; and let the Agent turns them into tool-based UI actions and checks on web and mobile.

[![RoboCon 2026 – What if Robot Framework Had a Brain](https://img.shields.io/badge/RoboCon%202026-What%20if%20Robot%20Framework%20Had%20a%20Brain-orange?style=for-the-badge)](https://www.robocon.io/agenda/helsinki#what-if-robot-framework-have-a-brain)

Alpha — An evolving experiment, with varying levels of maturity across keywords - Not recommended for production yet.

## Quick Start

```robot
*** Settings ***
Library    Agent    llm_client=openai    llm_model=gpt-4.1    platform_type=mobile    element_source=accessibility

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

# Web testing (coming soon)
pip install robotframework-agent[web]

# Mobile testing (+ Appium)
pip install robotframework-agent[mobile]

# Development (all tools)
pip install robotframework-agent[dev]
```

## LLM Providers

Supports OpenAI (default), Anthropic Claude, and Google Gemini.

```bash
# With Anthropic/Claude
pip install robotframework-agent[anthropic]

# With Google Gemini
pip install robotframework-agent[gemini]
```

```robot
# Use Claude
Library    Agent    llm_client=anthropic    llm_model=claude-sonnet-4

# Use Gemini
Library    Agent    llm_client=gemini    llm_model=gemini-2.0-flash
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

Experiments and design choices are informed by research on AI agents and UI perception:
- Support Vision-based UI parsing using OmniParser for element detection
- Set-of-Mark (SoM) technique for visual grounding
- Multi-provider LLM support (OpenAI, Anthropic, Gemini)

Ideas are tested and refined in [AgentArena](https://github.com/aidriventesting/AgentArena), our experimental testing environment.

## Presented at RoboCon 2026 (Helsinki)

This project will be showcased at RoboCon 2026 during the talk **"What if Robot Framework Had a Brain?"**  
👉 https://www.robocon.io/agenda/helsinki#what-if-robot-framework-have-a-brain


## Contributing

Builders, testers, and curious minds welcome.
Code, issues, and real-world use cases help shape the project.