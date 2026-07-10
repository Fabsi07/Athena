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

Later phases add, in order: Feature Platform & Research, Backtesting & Experiment Tracking, Risk
Engine & Paper Trading, AI Research Assistant, Multi-Agent Research, Live Trading (see
[[Roadmap]]). **Each layer only depends on the layers before it**:

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
| `risk/` | Risk engine, position sizing, kill switch, portfolio risk controls — independent of strategy code, final authority over position sizing/execution approval | ⬜ Not started |
| `paper_trading/` | Simulated live trading against real-time data | ⬜ Not started |
| `agents/` | AI-assisted analysis, critique, summarization, research workflows | ⬜ Not started |
| `docs/` | Design notes, assumptions, experiment summaries, operating rules | ✅ Exists |

> [!tip] Is this folder tree mandatory?
> Per [[Open Questions Log#Q29 — Repository layout — binding or illustrative?|Q29]], treat it as
> **illustrative**, not a binding contract — the current repo (`backend/data/adapters/`, etc.)
> already diverges slightly from an earlier doc's example tree. What's non-negotiable is that each
> module keeps one clear responsibility and the dependency direction above is respected.

## Repository layout as it exists today (`main`)

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

> [!note] Merged to `main`
> This tree was originally built on the `athena/v1-data-ingestion` branch and has since been
> merged into `main` (PR #1), along with the Obsidian vault itself (PR #2) and this vault-sync's
> own review-remediation branch.

## Related
- [[Exchange Adapter Pattern]]
- [[Long-Term Architecture & Development Order]]
- [[TimescaleDB Storage]]

#athena/architecture
