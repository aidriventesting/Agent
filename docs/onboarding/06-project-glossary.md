# Project glossary

**Agent**: AI component that interacts with the app to execute tests.

**Action**: one concrete UI operation (tap, type, scroll, wait).

**Agent.Do**: keyword that performs a single action.

**Agent.Check**: keyword that validates what is on screen (visual or structural).

**Observation**: raw data captured from the app (screenshot, DOM/tree, logs).

**UIState**: structured representation of the current screen and elements.

**Plan**: ordered list of steps to achieve a goal (future versions).

**Step**: higher-level intent in a plan (future versions).

**Executor**: module that turns a step into actions.

**Verifier / Critic**: module that decides if a step succeeded.

**Self-healing**: finding replacement locators when expected ones fail.

**Flakiness**: test instability unrelated to real product bugs.

**Artifacts**: screenshots, logs, traces, reports produced during runs.

**Eval suite**: fixed set of flows used to measure agent performance.

