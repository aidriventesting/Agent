# How we work

This project mixes automation engineering and AI. To stay sane, we use strict boundaries and evaluation.

## Branching & PRs

- Work on feature branches.
- Open PRs early.
- PR title should say what changed and why.

## Definition of done

A feature is "done" when:

- Code is merged with review.
- Public keywords are documented or updated.
- At least one test is added/updated.
- Eval suite does not regress on:
  - success rate
  - flakiness
  - cost (tokens/time)
- Artifacts and logs remain readable.

## Coding style

- Keep primitives simple and deterministic.
- Separate "reasoning" from "executing".
- Don't bake assumptions into tools; keep them in planner/logic.
- Prefer structured JSON I/O over free text from models.

## Adding or changing a keyword

When you add/modify a keyword (e.g., `Agent.Do`):

- Update keyword reference docs.
- Add a minimal example in tests.
- Ensure backward compatibility where possible.

## Evaluation mindset

We treat evaluation as part of development:

- Every meaningful change must be measurable.
- If the agent gets "smarter", we prove it with numbers.

## Communication

- Keep design decisions short and written.
- Use ADRs for big architectural choices.
- If something feels ambiguous, write it down early.

