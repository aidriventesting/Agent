# Robot Framework Agent

Robot Framework Agent is an open-source experiment to bring intent-level, LLM-augmented automation directly into Robot Framework suites. The goal is simple: describe what should happen in natural language and let the agent turn that intent into Appium/Selenium actions, visual checks, and future autonomous behaviors. No hype—just a practical attempt to give Robot Framework a “brain” testers can actually use.

[![RoboCon 2026 – What if Robot Framework Had a Brain](https://img.shields.io/badge/RoboCon%202026-What%20if%20Robot%20Framework%20Had%20a%20Brain-orange?style=for-the-badge)](https://www.robocon.io/agenda/helsinki#what-if-robot-framework-have-a-brain)

## Project Status & Vision

This repository is an ongoing exploration toward building a practical agentic toolkit for software testers.

**Current focus**  
- `Agent.Do` — interpret natural-language actions  
- `Agent.Check` — interpret natural-language assertions

Both keywords are in active development. Work is underway to make them stable, predictable, and usable on real production application.

**Near-term goals**  
- add mid-level capabilities such as locating visual/semantic elements  
- extend `Agent.ReportBug` so legacy suites (without agentic capabilities) can file actionable reports automatically  
- expose internal locator/vision data for debugging  
- experiment with autonomous behaviours in controlled, test-safe ways

None of this is final; the library is evolving through experiments, refactoring, and real-world usage. Contributions, critiques, and field tests are welcome.

## Presented at RoboCon 2026 (Helsinki)

This project will be showcased at RoboCon 2026 during the talk **“What if Robot Framework Had a Brain?”**  
👉 https://www.robocon.io/agenda/helsinki#what-if-robot-framework-have-a-brain

The session will cover the architecture behind the agent, early field results, and how intent-based keywords can help teams work at a higher abstraction level without abandoning Robot Framework’s strengths.

## Support & Sponsorship

If you find this work useful, inspiring, or simply want to help move agentic testing forward, you can support the project by:

- sponsoring dedicated development time   
- funding compute for VLM/LLM experimentation  
- contributing code, test cases, or research notes

This is not a finished product; it’s an open laboratory for building smarter testing tools. Any support—small or large—helps the project grow and stay independent.

## Overview

Robot Framework Agent exposes high-level keywords to describe actions and checks in natural language; the agent then translates them into Appium (real device/emulator) and other UI interactions.

## Usage (Robot Framework)

In your `.robot` file:

```robot
*** Settings ***
Library    Agent    llm_client=openai    llm_model=gpt-4o-mini

*** Test Cases ***
Agent Example
    Agent.Do      accept cookies
    Agent.Check   the screen correctly shows the Homepage
```

### Notes
- Provided keywords: `Agent.Do <instruction>`, `Agent.Check <instruction>`.
- Works with real mobile devices and BrowserStack; see more details below.

## Running Tests on BrowserStack

### Prerequisites
1. BrowserStack Account
   - Sign up at browserstack.com if you don't have an account
   - Get your username and access key from BrowserStack dashboard

2. Environment Setup
   ```bash
   # Install required dependencies
   pip install -r requirements.txt
   pip install browserstack-sdk
   ```

3. Configuration
   - Create/update `browserstack.yml` in your project root
   - Configure your credentials:
     ```yaml
     userName: YOUR_USERNAME
     accessKey: YOUR_ACCESS_KEY
     ```
   - Update app path with your app's BrowserStack URL:
     ```yaml
     app: bs://YOUR_APP_ID
     ```

### Running Tests
1. Single Test Execution
   ```bash
   browserstack-sdk robot tests/atest/your_test.robot
   ```

2. Running Test Suites
   ```bash
   browserstack-sdk robot tests/atest/
   ```

3. Parallel Execution
   ```bash
   browserstack-sdk robot --variable parallel_execution:true tests/atest/
   ```

### Device Configuration
- Edit `browserstack.yml` to specify target devices:
  ```yaml
  platforms:
    - deviceName: Samsung Galaxy S21
      platformVersion: 12.0
      platformName: Android
    # Add more devices as needed
  ```

### Development Tips
1. Debug Mode
   - Set `debug: true` in browserstack.yml
   - Enable detailed logs: `consoleLogs: info`

2. Local Testing
   - For testing with local apps/servers:
     ```yaml
     browserstackLocal: true
     ```

3. Build Identification
   - Set unique build names for tracking:
     ```yaml
     buildName: "Dev Build"
     buildIdentifier: ${BUILD_NUMBER}
     ```

### Viewing Results
1. Real-time monitoring: BrowserStack dashboard
2. Test reports: Available in `log/` directory after execution
3. Session videos: Automatically recorded and available in BrowserStack dashboard