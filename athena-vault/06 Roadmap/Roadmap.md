---
title: Roadmap
tags: [athena, roadmap]
source: docs/ROADMAP.md, CLAUDE.md
---

# Roadmap

Mirrors the [[Long-Term Architecture & Development Order#Preferred development order|Preferred
Development Order]] in `CLAUDE.md`. Each phase should be solid — tested, reviewed, and
trustworthy — before the next one starts.

| Phase | Name | Status |
|---|---|---|
| 0 | Project Foundation | ✅ Done |
| 1 | Data Ingestion & Data Quality | 🟡 In progress |
| 2 | Backtesting | ⬜ Not started |
| 3 | Experiment Tracking | ⬜ Not started |
| 4 | Paper Trading | ⬜ Not started |
| 5 | AI Research Assistant | ⬜ Not started |
| 6 | Multi-Agent Research Layer | ⬜ Not started |
| 7 | Live Trading | ⬜ Not started |

---

## Phase 0 — Project Foundation

Governance docs, directory layout, toolchain (`uv`, `pytest`, Docker Compose for TimescaleDB). No
trading-relevant code.

**Status: ✅ Done** — `CLAUDE.md`, `AGENTS.md`, `pyproject.toml`, `docker-compose.yml` all exist.

## Phase 1 — Data Ingestion & Data Quality

Exchange adapters (`Exchange` base class, `BybitExchange`, `BinanceExchange`), validated schemas,
idempotent TimescaleDB storage. A [[AI Agent Policy#The only agent approved for V1: Data Quality Agent|Data Quality Agent]]
that checks candle completeness, missing values, outliers, and Binance/Bybit price divergence
belongs here once ingestion is stable.

**Status: 🟡 In progress** — see [[Data Sources]], [[Exchange Adapters]], [[Schemas]],
[[TimescaleDB Storage]] for what exists. The Data Quality Agent itself is not built yet, and
several ingestion-scope questions remain open (see [[Open Questions Log]]).

## Phase 2 — Backtesting

A backtesting engine with realistic fills (conservative by default — see
[[Trading Research Rules]]), fees, and slippage, developed alongside feature engineering and
strategy research as one iterative loop.

**Status: ⬜ Not started.** Blocked on several open decisions: default fee/slippage values,
position sizing model, overfitting-detection thresholds, mandatory benchmark — see
[[Open Questions Log#BACKTESTING.md|the BACKTESTING.md questions]].

## Phase 3 — Experiment Tracking

Reproducible experiment records: data version, code version, parameters, and results, so no
backtest result is ever un-reproducible.

**Status: ⬜ Not started.**

## Phase 4 — Paper Trading

Simulated execution against live data, with the same risk controls a live system would use, before
any real capital is at risk.

**Status: ⬜ Not started.** Blocked on Risk Engine defaults (position size limits, daily loss,
drawdown, kill-switch thresholds — see [[Open Questions Log#RISK_ENGINE.md|RISK_ENGINE.md questions]])
and default starting virtual capital ([[Open Questions Log#Q22 — Default starting virtual capital|Q22]]).

## Phase 5 — AI Research Assistant

AI assists with hypothesis generation, result summarization, and flaw identification — never with
placing trades or sizing positions from natural-language confidence. See [[AI Agent Policy]].

**Status: ⬜ Not started.** Explicitly step-7-adjacent work; LLM provider/spend ceiling
undecided — see [[Open Questions Log#Q03 — LLM provider/model|Q03]].

## Phase 6 — Multi-Agent Research Layer

Multiple agents debating and cross-checking hypotheses. Only pursued once the single-agent
research loop is proven useful.

**Status: ⬜ Not started.** Per [[Open Questions Log#Q34 — AGENT_PROTOCOL / AI_ARCHITECTURE staging|Q34]],
the original `AGENT_PROTOCOL.md` / `AI_ARCHITECTURE.md` design docs describe this phase's
target state only — nothing to implement yet.

## Phase 7 — Live Trading

Live trading only after strict validation, paper trading, risk controls, and explicit human
approval. Not started until every prior phase is mature.

**Status: ⬜ Not started, by design.**

## Related
- [[Long-Term Architecture & Development Order]]
- [[Open Questions Log]]
- [[North Star]]

#athena/roadmap
