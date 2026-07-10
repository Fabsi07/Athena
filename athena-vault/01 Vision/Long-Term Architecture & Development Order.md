---
title: Long-Term Architecture & Development Order
tags: [athena, vision, architecture]
source: CLAUDE.md, AGENTS.md
---

# Long-Term Architecture & Development Order

## Long-term architecture

The distributed, multi-agent end-state Project Athena is aimed at — **not** what Version 1
builds.

```
WebSocket → Kafka / RabbitMQ → Collector → TimescaleDB → Feature Store → Research Layer
```

> [!warning] Do not build this early
> If asked to build a complex agent system or distributed infrastructure (like Kafka/RabbitMQ)
> early, the correct response is to refuse and first create the smaller, local TimescaleDB
> foundation it needs. This is an explicit instruction in `CLAUDE.md`, not a suggestion.

Every architectural choice in [[System Architecture & Repository Layout]] is deliberately a
**subset** of this diagram:

| Long-term component | V1 equivalent | Status |
|---|---|---|
| WebSocket ingestion | REST polling via [[Exchange Adapter Pattern]] | ✅ Bybit/Binance candles + Bybit funding |
| Kafka / RabbitMQ | *(skipped entirely for V1)* | ⬜ Not started, not planned soon |
| Collector | Adapter + script (`scripts/ingest_bybit_funding.py`) | ✅ Minimal version exists |
| TimescaleDB | TimescaleDB (same) | ✅ Schema + idempotent writer exist |
| Feature Store | `features/` (planned) | ⬜ [[Roadmap#Phase 2 — Feature Platform & Research\|Phase 2]] |
| Research Layer | `research/`, `backtesting/`, `strategies/` (planned) | ⬜ Not started |

A message broker only becomes justified once there are multiple independent consumers of the same
live stream (e.g. live paper trading *and* a Data Quality Agent *and* a dashboard, all reading the
same feed concurrently). Until that real requirement exists, direct ingestion into TimescaleDB is
simpler, cheaper, and easier to debug.

## Preferred development order

Work in this order unless explicitly told otherwise. This mirrors `docs/ROADMAP.md`, which is the
**authoritative implementation order** — each step should be solid before the next starts (see
[[Roadmap]] for the phase-by-phase detail):

0. **Project Foundation** — repository structure, coding standards, governance, dev environment, service interfaces. No trading logic.
1. **Data Platform** — exchange adapters, ingestion, TimescaleDB, historical backfill, scheduler, data validation, Data Quality Service, collector monitoring, initial dashboard, logging/observability.
2. **Feature Platform & Research** — Feature Factory, Feature Registry, feature versioning, indicator generation, research workflows, dataset versioning.
3. **Backtesting & Experiment Tracking** — developed together: backtesting engine, portfolio simulation, risk-adjusted metrics, Buy & Hold benchmark, experiment tracking, result reproducibility.
4. **Risk Engine & Paper Trading** — risk engine, position sizing, kill switch, portfolio controls, paper trading, live monitoring, dashboard expansion.
5. **AI Research Assistant** — research assistant, documentation assistant, experiment summaries, hypothesis generation, critique support.
6. **Multi-Agent Research** — multi-agent discussions, consensus evaluation, architecture/code review agents, research debate, evidence aggregation. Only after Phase 5 has demonstrated clear value.
7. **Live Trading** — only after strict validation, a validated risk engine, successful paper trading, and explicit human approval.

> [!note] Earlier version of this order
> An earlier version of this list gave Risk & Metrics its own numbered step *before* experiment
> tracking, while the roadmap of the time didn't have a matching phase for it — a pre-implementation
> architecture review flagged that mismatch. The order above and [[Roadmap]] are now kept in sync:
> Risk Engine is grouped with Paper Trading (Phase 4), and Backtesting is grouped with Experiment
> Tracking (Phase 3).

> [!danger] Staging rule
> `AGENT_PROTOCOL.md` and `AI_ARCHITECTURE.md` (from the original design doc set) describe a
> fully built multi-agent system. Per [[Open Questions Log#Q34 — AGENT_PROTOCOL / AI_ARCHITECTURE staging|Q34]],
> these are step-7 target-state specs only — nothing in them should be implemented until steps 1–6
> are complete.

## Related
- [[North Star]]
- [[System Architecture & Repository Layout]]
- [[Roadmap]]

#athena/vision #athena/architecture
