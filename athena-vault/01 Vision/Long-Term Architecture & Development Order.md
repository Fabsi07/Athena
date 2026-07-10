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
| Feature Store | `features/` (planned) | ⬜ [[Roadmap#Phase 2 — Backtesting\|Phase 2]] |
| Research Layer | `research/`, `backtesting/`, `strategies/` (planned) | ⬜ Not started |

A message broker only becomes justified once there are multiple independent consumers of the same
live stream (e.g. live paper trading *and* a Data Quality Agent *and* a dashboard, all reading the
same feed concurrently). Until that real requirement exists, direct ingestion into TimescaleDB is
simpler, cheaper, and easier to debug.

## Preferred development order

Work in this order unless explicitly told otherwise. Each step should be solid before the next
starts (see [[Roadmap]] for the phase-by-phase detail):

1. **Data ingestion** — Binance, Bybit, FRED, CoinGecko, Alternative.me
2. **Data validation and local storage** — via TimescaleDB
3. **The Iterative Loop** — Backtesting Engine ↔ Feature Engineering ↔ Strategy Research
4. **Independent Risk & Metrics Module**
5. **Experiment tracking**
6. **Paper trading** — simulated execution on live data
7. **AI research assistant and multi-agent debate**
8. **Live trading controls**

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
