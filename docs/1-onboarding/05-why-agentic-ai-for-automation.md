# Why agentic AI for testing?

Classic automation is powerful but rigid: it executes exactly what you coded.

An agentic AI adds reasoning and flexibility.

## What an agent does

The agent:
1. **Understands intent**: "Click the submit button" vs `xpath=//button[3]`
2. **Observes the UI**: Takes screenshots, reads element trees
3. **Decides actions**: Which element matches the intent?
4. **Performs actions**: Via Appium/Playwright
5. **Verifies outcomes**: Did it work? Should we retry?
6. **Recovers from changes**: Finds alternatives when locators break

## What "agentic" means here

Not sci-fi autonomy. Practically:

- A loop of **observe → reason → act → check**
- Bounded by tools and rules
- Producing deterministic artifacts for debugging
- Controlled by test cases (not wandering on its own)

## Problems this approach solves

### 1. Self-healing locators

**Traditional**:
```robot
Click Button    id=submit-btn  # ❌ Breaks when ID changes
```

**With agent**:
```robot
Agent.Do    Click the blue submit button
# ✓ Works even if ID changes
# Agent uses: text, color, position, visual appearance
```

### 2. Dynamic data handling

**Traditional**:
```robot
Page Should Contain    5 new messages  # ❌ Fails when count changes
```

**With agent**:
```robot
Agent.Check    The page shows new messages
# ✓ Validates intent, not exact text
```

### 3. Smart waiting

**Traditional**:
```robot
Sleep    3s
Click Button    id=load-more  # ❌ Still flaky, wastes time
```

**With agent**:
```robot
Agent.Do    Click the load more button
# ✓ Observes screen, waits for element to be ready
```

### 4. Environment-agnostic assertions

**Traditional**:
```robot
Page Should Contain    Welcome, John Doe  # ❌ Fails in staging
```

**With agent**:
```robot
Agent.Check    User is logged in successfully
# ✓ Adapts to different welcome messages
```

### 5. Cross-platform support

**Traditional**:
```robot
# Web test
Click Element    id=menu

# Android test  
Click Element    resource-id=com.app:id/menu

# iOS test
Click Element    accessibility id=Menu
```

**With agent**:
```robot
# Works everywhere
Agent.Do    Open the menu
```

### 6. Visual validation

**Traditional**:
```robot
Page Should Contain Element    id=map  # ✓ Map exists
# ❌ Can't verify map content
```

**With agent**:
```robot
Agent.Check    The map shows the user's location in Paris
# ✓ Uses vision models to verify content
```

### 7. Accessibility-friendly

**Traditional**:
```robot
Click Element    xpath=//android.widget.Button[3]  # ❌ Fragile
```

**With agent**:
```robot
Agent.Do    Tap the third button
# ✓ Uses visual understanding, not brittle XPath
```

### 8. Rich failure diagnosis

**Traditional**:
```
FAIL: Element 'id=submit' not found
```

**With agent**:
```
FAIL: Could not find submit button
Screenshot: artifacts/step_15.png
Reasoning: Expected blue button with text "Submit" 
           but page shows error message "Form incomplete"
Elements found: [Cancel, Back, Help]
Suggestion: Check if validation passed before submit
```

## Scope of V1

V1 focuses on **two primitives**:

### Agent.Do
Perform a single UI action with natural language.

```robot
Agent.Do    Type "hello" in the search box
Agent.Do    Scroll down to the footer
Agent.Do    Tap the settings icon in the top right
```

### Agent.Check  
Verify the UI state using visual and semantic reasoning.

```robot
Agent.Check    The login was successful
Agent.Check    The cart contains 3 items
Agent.Check    The error message is displayed
```

## What V1 does NOT include (yet)

- **Full autonomy**: "Test the checkout flow" without steps
- **Planning**: Breaking high-level goals into steps
- **Memory**: Learning from previous runs
- **Self-improvement**: Updating tests automatically

These come in future versions. V1 proves the primitives work.

## How it works under the hood

1. **Test calls** `Agent.Do "Click login"`
2. **Agent captures** screenshot + element tree
3. **LLM reasons**: "Login button is at coordinates (350, 120), has id=login-btn"
4. **Agent executes** via Appium/Selenium
5. **Agent verifies** action succeeded
6. **Logs artifacts**: screenshot, reasoning, outcome

## Evaluation-driven development

We measure agent performance on:
- **Success rate**: % of actions that work
- **Cost**: Tokens and time per action
- **Flakiness**: How often same action fails randomly
- **Maintenance**: How often tests break on UI changes

Every change must prove it doesn't regress these metrics.

## Summary: AI + automation

| **Problem** | **Traditional** | **With Agent** |
|-------------|-----------------|----------------|
| Locator breaks | Manual fix | Self-healing |
| Dynamic data | Fails | Semantic validation |
| Timing | Hardcoded waits | Observes & adapts |
| Visual content | Not testable | Vision models |
| Cross-platform | 3 test suites | 1 test suite |
| Debugging | Screenshot only | Screenshot + reasoning |

The agent doesn't replace Selenium/Appium — it makes them intelligent.

