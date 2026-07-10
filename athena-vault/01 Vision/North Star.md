---
title: North Star
tags: [athena, vision]
source: CLAUDE.md, AGENTS.md
---

# North Star

Project Athena is a **reproducible quant research platform** for discovering, testing, and
validating systematic trading hypotheses — not a trading bot, and not (yet) anything that touches
real money.

> [!quote] From `AGENTS.md`
> Treat "autonomous multi-agent trading AI" as the long-term vision, not the first implementation
> milestone.

## Immediate goal

> Build a lean, reliable research platform utilizing $0 budget, free-tier data sources and a
> local database architecture.

## What the system must be able to do, eventually

- Collect reliable market data
- Run realistic backtests
- Track every experiment
- Compare strategies against benchmarks
- Reject weak ideas quickly
- Promote only validated candidates to paper trading
- Eventually support agent-assisted research

## Hard constraint

> The system should not place live trades until research, validation, paper trading, risk
> controls, and human approval are mature.

This is not a soft preference — see [[Coding Guidelines & Operating Principles]] and [[AI Agent Policy]] for the rules
that enforce it in code and process.

## Build philosophy

> If there is a conflict between building something impressive and building something measurable,
> choose measurable.

Practically:
- Prefer a lean research platform over complex AI automation or heavy DevOps infrastructure.
- Do not introduce a large framework unless the project clearly needs it.
- Keep trading logic separate from execution logic; keep research code separate from live-trading
  code.
- Assume financial backtests are fragile until proven otherwise (see [[Trading Research Rules]]).

## Related
- [[Long-Term Architecture & Development Order]]
- [[Coding Guidelines & Operating Principles]]

#athena/vision
