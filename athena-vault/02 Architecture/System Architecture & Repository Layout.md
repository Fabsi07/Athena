---
title: System Architecture & Repository Layout
tags: [athena, architecture]
source: docs/ARCHITECTURE.md, AGENTS.md
---

# System Architecture & Repository Layout

## Current target data flow

```
Exchange API -> Exchange Adapter -> validated Records (pydantic) -> TimescaleDB -> idempotent storage
```

Later phases add, in order: Feature Engineering, Backtesting, Experiment Tracking, Paper Trading,
Agents, Live Trading (see [[Roadmap]]). **Each layer only depends on the layers before it**:

- A backtest never depends on a UI.
- A strategy never fetches live data on its own.
- A research agent never executes trades.

## Layer boundaries (`AGENTS.md` Architecture Principles)

| Directory | Responsibility | Status |
|---|---|---|
| `backend/data/` | Collectors, normalization, storage adapters | ✅ Exists — see [[Data Sources]] |
| `research/` | Notebooks, experiments, hypotheses, exploratory scripts | ⬜ Not started |
| `backtesting/` | Strategy simulation, cost models, metrics, validation | ⬜ Not started |
| `features/` | Feature generation and feature validation | ⬜ Not started |
| `strategies/` | Strategy definitions and parameter sets | ⬜ Not started |
| `paper_trading/` | Simulated live trading against real-time data | ⬜ Not started |
| `agents/` | AI-assisted analysis, critique, summarization, research workflows | ⬜ Not started |
| `docs/` | Design notes, assumptions, experiment summaries, operating rules | ✅ Exists |

> [!tip] Is this folder tree mandatory?
> Per [[Open Questions Log#Q29 — Repository layout — binding or illustrative?|Q29]], treat it as
> **illustrative**, not a binding contract — the current repo (`backend/data/adapters/`, etc.)
> already diverges slightly from an earlier doc's example tree. What's non-negotiable is that each
> module keeps one clear responsibility and the dependency direction above is respected.

## Repository layout as it exists today (`athena/v1-data-ingestion` branch)

```
backend/
  data/
    adapters/
      base.py         # Exchange ABC — see Exchange Adapter Pattern
      binance.py       # BinanceExchange — candles only
      bybit.py          # BybitExchange — candles + funding
    schemas.py          # CandleRecord, FundingRecord (pydantic)
    storage/
      schema.sql         # TimescaleDB DDL
      timescale_writer.py # idempotent writer, zero transformation
scripts/
  ingest_bybit_funding.py  # CLI wiring adapter -> storage
docs/
  ARCHITECTURE.md, PRINCIPLES.md, ROADMAP.md
tests/
  test_bybit_adapter.py, test_schemas.py, test_timescale_writer.py
docker-compose.yml     # local TimescaleDB, pinned image tag
pyproject.toml         # uv + pytest config
```

> [!note] Not yet merged to `main`
> This tree exists on the `athena/v1-data-ingestion` branch. `main` currently only tracks
> `.gitignore`, `AGENTS.md`, and `CLAUDE.md`.

## Related
- [[Exchange Adapter Pattern]]
- [[Long-Term Architecture & Development Order]]
- [[TimescaleDB Storage]]

#athena/architecture
