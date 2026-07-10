---
title: Roadmap
tags: [athena, roadmap]
source: docs/ROADMAP.md, CLAUDE.md
---

# Roadmap

Mirrors `docs/ROADMAP.md`, which is the **authoritative implementation order** (also mirrored in
[[Long-Term Architecture & Development Order#Preferred development order|CLAUDE.md/AGENTS.md's
Preferred Development Order]]). Each phase should be functionally complete, tested, documented,
and reviewed before the next one starts. The architecture is a **modular monolith** in V1, with
every module designed so it can later evolve into an independent microservice without changing its
public contracts.

| Phase | Name | Status |
|---|---|---|
| 0 | Project Foundation | ✅ Done |
| 1 | Data Platform | 🟡 In progress |
| 2 | Feature Platform & Research | ⬜ Not started |
| 3 | Backtesting & Experiment Tracking | ⬜ Not started |
| 4 | Risk Engine & Paper Trading | ⬜ Not started |
| 5 | AI Research Assistant | ⬜ Not started |
| 6 | Multi-Agent Research | ⬜ Not started |
| 7 | Live Trading | ⬜ Not started |

> [!note] Renamed/regrouped from an earlier roadmap version
> Backtesting and Experiment Tracking are now developed together as one phase (3), and Risk Engine
> now has its own explicit phase grouped with Paper Trading (4) — an earlier roadmap version left
> the Risk Engine's place in the sequence ambiguous, which a pre-implementation architecture review
> flagged and this restructure fixes.

---

## Phase 0 — Project Foundation

Repository structure, coding standards, project governance, dev environment (`uv`, `pytest`,
Docker Compose, TimescaleDB), CI-ready layout, service interfaces and dependency boundaries. No
trading logic.

**Status: ✅ Done** — `CLAUDE.md`, `AGENTS.md`, `pyproject.toml`, `docker-compose.yml` all exist.

## Phase 1 — Data Platform

Exchange adapters (Binance, Bybit, Coinbase reference), data ingestion, TimescaleDB, historical
backfill, scheduler, data validation, Data Quality Service, collector monitoring, initial
dashboard, logging and observability.

**Status: 🟡 In progress** — see [[Data Sources]], [[Exchange Adapters]], [[Schemas]],
[[TimescaleDB Storage]] for what exists. The Data Quality Service/Agent, scheduler, backfill, and
dashboard are not built yet. Most of the ingestion-scope questions that used to block this phase
are now resolved — see [[Open Questions Log]] (Q06, fee/slippage defaults, is the one still
explicitly deferred, and it blocks Phase 3 rather than this phase).

## Phase 2 — Feature Platform & Research

Feature Factory, Feature Registry, feature versioning, indicator generation, research workflows,
dataset versioning. Goal: every feature is reproducible and versioned.

**Status: ⬜ Not started.** Required V1 feature set and versioning scheme are resolved — see
[[Open Questions Log#Q17 — Required V1 feature set and default parameters|Q17]] and
[[Open Questions Log#Q18 — Feature version numbering scheme|Q18]].

## Phase 3 — Backtesting & Experiment Tracking

Developed together: backtesting engine, portfolio simulation, risk-adjusted metrics, Buy & Hold
benchmark, experiment tracking, result reproducibility — realistic fills, fees, and slippage,
conservative by default (see [[Trading Research Rules]]).

**Status: ⬜ Not started.** Position sizing model, overfitting-detection thresholds, and the
mandatory benchmark are resolved — see [[Open Questions Log#BACKTESTING.md|the BACKTESTING.md
questions]]. Default fee/slippage values
([[Open Questions Log#Q06 — Default fee and slippage values|Q06]]) remain explicitly deferred and
are the one open blocker for this phase, since `docs/PRINCIPLES.md` requires fees and slippage in
every backtest.

## Phase 4 — Risk Engine & Paper Trading

Risk engine, position sizing, kill switch, portfolio controls, paper trading, live monitoring,
dashboard expansion. Goal: operate safely without risking real capital.

**Status: ⬜ Not started.** Risk Engine defaults (position size limits, daily loss, drawdown,
kill-switch thresholds) and default starting virtual capital are now resolved — see
[[Open Questions Log#RISK_ENGINE.md|RISK_ENGINE.md questions]] and
[[Open Questions Log#Q22 — Default starting virtual capital|Q22]].

## Phase 5 — AI Research Assistant

Research assistant, documentation assistant, experiment summaries, hypothesis generation, critique
support. AI never executes trades, changes risk limits, or bypasses human oversight. See
[[AI Agent Policy]].

**Status: ⬜ Not started.** LLM provider/spend ceiling resolved as provider-agnostic, disabled by
default, $0 hard limit until explicitly configured — see
[[Open Questions Log#Q03 — LLM provider/model|Q03]].

## Phase 6 — Multi-Agent Research

Multi-agent discussions, consensus evaluation, architecture/code review agents, research debate,
evidence aggregation. Only pursued once Phase 5 has demonstrated clear value.

**Status: ⬜ Not started.** Per [[Open Questions Log#Q34 — AGENT_PROTOCOL / AI_ARCHITECTURE staging|Q34]],
the original `AGENT_PROTOCOL.md` / `AI_ARCHITECTURE.md` design docs describe this phase's
target state only — nothing to implement yet.

## Phase 7 — Live Trading

The final milestone. Requires a stable data platform, proven backtesting, reliable experiment
tracking, a validated risk engine, successful paper trading, and explicit human approval. Remains
optional and must never become the default operating mode.

**Status: ⬜ Not started, by design.**

## Long-term evolution

Version 1 is a modular monolith. As Athena matures, individual bounded contexts may be extracted
into independent microservices without changing business logic or service contracts — potential
future services: Data Service, Feature Service, Research Service, Backtesting Service, Risk
Service, Paper Trading Service, AI Service, Dashboard/API Gateway. See
[[System Architecture & Repository Layout]].

## Related
- [[Long-Term Architecture & Development Order]]
- [[Open Questions Log]]
- [[North Star]]

#athena/roadmap
