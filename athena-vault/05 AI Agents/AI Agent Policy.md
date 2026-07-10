---
title: AI Agent Policy
tags: [athena, ai-policy]
source: CLAUDE.md, AGENTS.md
---

# AI Agent Policy

> [!danger] Core rule
> AI can assist research, but it must not be treated as a magic signal engine.

## Good AI uses

- **Monitoring data quality** (the [[#The only agent approved for V1: Data Quality Agent|Data Quality Agent]])
- Proposing strategy ideas
- Summarizing experiment results
- Identifying possible flaws
- Comparing hypotheses
- Generating test plans
- Explaining code
- Reviewing research assumptions

## Bad AI uses — explicitly forbidden

- Inventing market facts
- Making unsupported predictions
- Hiding uncertainty
- Placing trades
- Bypassing risk controls
- Converting natural-language confidence into position size

## The only agent approved for V1: Data Quality Agent

Per `AGENTS.md`, this is the **only permitted early-stage AI agent**. Its job is exclusively to
monitor data integrity and alert on issues. It must rigorously verify:

- Are candles complete?
- Are there missing values or outliers?
- Do prices align approximately between Binance and Bybit? — this is why
  [[Exchange Adapters#`BinanceExchange` (`backend/data/adapters/binance.py`)|`BinanceExchange`]]
  exists at all in its current minimal form: just enough to cross-check Bybit prices.
- Have WebSocket connections failed?
- Were duplicate records stored?

Everything else agent-related (Research Agent, Documentation Agent, Code Review Agent, Experiment
Review Agent, Architecture Assistant) is **step-7 work** — see
[[Open Questions Log#Q04 — V1 agent set|Q04]] and
[[Long-Term Architecture & Development Order#Preferred development order|Development Order]].
Nothing in that category should be built until data, backtesting, risk, and paper trading are
mature.

## Required structure for any agent's output

If implementing agents, use structured outputs — not free-form prose:

```text
agent_name:
hypothesis:
input_data:
signal:
confidence:
evidence:
counterarguments:
known_limitations:
recommended_next_test:
```

Note: the representation and semantics of `confidence` are still an open question — see
[[Open Questions Log#Q02 — Confidence semantics|Q02]]. The working recommendation is a plain
self-reported float 0.0–1.0, since there's no ground truth to derive it from, and per policy it
must never feed position sizing regardless of its value.

## Related
- [[Trading Research Rules]]
- [[Roadmap#Phase 5 — AI Research Assistant|Phase 5]]
- [[Roadmap#Phase 6 — Multi-Agent Research Layer|Phase 6]]

#athena/ai-policy
