---
title: Coding Guidelines & Operating Principles
tags: [athena, principles, coding-standards]
source: CLAUDE.md, AGENTS.md
---

# Coding Guidelines & Operating Principles

## Coding guidelines (`CLAUDE.md`)

- Inspect the repository before changing files.
- Keep implementations modular.
- Enforce the [[Exchange Adapter Pattern]] — no hardcoded API calls in research files.
- Prefer boring, reliable code over clever abstractions.
- Use explicit schemas and typed interfaces where practical (see [[Schemas]]).
- Separate research, backtesting, paper trading, and live execution — see
  [[System Architecture & Repository Layout]].
- Avoid hidden global state.
- Avoid strategy code that fetches data implicitly.
- Make experiments reproducible.
- Do not add dependencies casually.

## Agent behavior rules (`AGENTS.md`)

When working in this repository, AI agents and contributors are expected to:

- Read the existing project structure before making changes.
- Keep changes small, testable, and reversible.
- Not introduce a large framework unless the project clearly needs it.
- Prefer simple modules with explicit data contracts.
- Keep trading logic separate from execution logic.
- Keep research code separate from live-trading code.
- Never let an AI-generated signal trade real funds directly.
- Assume financial backtests are fragile until proven otherwise.
- Watch aggressively for lookahead bias, survivorship bias, data snooping, and overfitting (see
  [[Trading Research Rules]]).

## Testing (currently unconfirmed defaults)

- Test framework: **pytest** is already in use (`pyproject.toml`, `tests/`), matching the
  recommendation in [[Open Questions Log#Q30 — Test framework|Q30]].
- Coverage target: not formally set — recommendation in
  [[Open Questions Log#Q31 — Coverage target|Q31]] is 80% overall, 90%+ for Risk Engine and
  Portfolio Accounting once those exist.
- What exists today: `tests/test_bybit_adapter.py` (mocked HTTP via `respx`),
  `tests/test_schemas.py`, `tests/test_timescale_writer.py`.

## Related
- [[Trading Research Rules]]
- [[System Architecture & Repository Layout]]
- [[Exchange Adapter Pattern]]

#athena/principles
