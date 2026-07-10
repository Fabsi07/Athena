---
title: Trading Research Rules
tags: [athena, principles, research-integrity]
source: CLAUDE.md, docs/PRINCIPLES.md
---

# Trading Research Rules

> [!danger] Always treat strategy results skeptically.
> This is the governing attitude for all research in Project Athena.

## Bias checklist — watch for these on every result

- **Lookahead bias** — using information that wouldn't have been available at decision time
- **Overfitting** — a strategy tuned to noise in one dataset
- **Data leakage** — train/test contamination
- **Survivorship bias** — only looking at assets/strategies that "survived"
- **Unrealistic fills** — assuming trades execute at prices that weren't actually achievable
- **Missing fees and slippage** — backtests that ignore real trading costs
- **Cherry-picked date ranges** — results that only hold over a hand-picked window
- **Parameter sensitivity** — a strategy that only works for one narrow parameter setting

## Result labeling — never blur these stages

Every result must be clearly labeled as one of:

1. **Hypothesis** — an untested idea
2. **Backtest result** — tested on historical data
3. **Out-of-sample result** — tested on data not used for tuning
4. **Paper-trading result** — simulated execution on live data
5. **Live-trading result** — real capital, real execution

> [!warning] Never imply a backtest guarantees future returns.

## Default fill assumptions — conservative by default

- **Market orders** cross the spread and include fees/slippage — this is the default.
- **Limit-order fill-at-touch** is optimistic and may **only** be used when explicitly labeled and
  justified in the experiment writeup.

Concrete defaults for fees/slippage/position sizing are still open — see
[[Open Questions Log#Q06 — Default fee and slippage values|Q06]] and
[[Open Questions Log#Q07 — Default position sizing model and initial capital|Q07]].

## Non-negotiable principles (`docs/PRINCIPLES.md`)

> When a proposed change conflicts with one of these, the principle wins.

- No live trades without explicit human approval.
- No strategy without a reproducible backtest.
- No backtest without fees, slippage, and conservative fill assumptions.
- No AI signal is ever the sole basis for a trading decision.
- Every external data source goes through an [[Exchange Adapter Pattern|Exchange adapter]] — no
  direct API calls from research, backtesting, or strategy code.
- Every experiment must be reproducible: fixed data version, fixed code version, fixed parameters,
  logged results.
- Raw data is preserved; cleaning and interpretation happen visibly, in reviewable code — never
  silently.
- Results are always labeled by stage (see above). A backtest result never implies future returns.

## Related
- [[AI Agent Policy]]
- [[Coding Guidelines & Operating Principles]]
- [[Open Questions Log]]

#athena/principles
