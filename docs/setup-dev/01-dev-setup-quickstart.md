# Dev setup quickstart

This is the minimal path to run the agent locally.

## Prerequisites

- Python 3.10+
- Robot Framework
- A UI automation backend:
  - **Web**: Playwright + a browser driver
  - **Mobile**: Appium + real device/emulator
- Access to an LLM provider (OpenAI/Azure/local), depending on config.

## Install

```bash
git clone <REPO_URL>
cd <REPO_NAME>

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

## Configure environment

Copy `env.example` to `.env` and set your keys/config.

## Run a sample suite

```bash
pytest tests/utest -q
```

## Outputs

After a run you should get:

- Robot log + report
- screenshots per step
- agent reasoning trace (if enabled)

Artifacts location:

```
./artifacts/<run_id>/...
```

## Common issues

- Appium/Selenium not running
- Wrong device/browser capabilities
- Missing API key / model name
- Permission issues for screenshots

