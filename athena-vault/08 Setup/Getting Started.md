---
title: Getting Started
tags: [athena, setup]
source: README.md (athena/v1-data-ingestion branch)
---

# Getting Started

> [!warning] Branch note
> Everything described here exists on the `athena/v1-data-ingestion` branch, **not** on `main`.
> `main` currently only tracks `.gitignore`, `AGENTS.md`, and `CLAUDE.md`.

## What you can actually run today

```bash
# install dependencies (uv-managed)
uv sync
uv run pytest

# local TimescaleDB
cp .env.example .env
docker compose up -d

# fetch Bybit funding-rate history and write it to TimescaleDB
uv run python scripts/ingest_bybit_funding.py \
    --symbol BTCUSDT --start 2024-01-01 --end 2024-01-02
```

## What this proves

- [[Exchange Adapters#`BybitExchange` (`backend/data/adapters/bybit.py`)|`BybitExchange`]] fetches
  real funding-rate data from Bybit's public V5 API.
- Every record passes through [[Schemas|`FundingRecord` validation]] before it's allowed near the
  database.
- [[TimescaleDB Storage#Writer (`backend/data/storage/timescale_writer.py`)|`TimescaleWriter`]]
  inserts it idempotently — running the same command twice does not duplicate rows.

## What this does NOT do

- No candles are ingested by the CLI script yet (only funding rates) — `BybitExchange.get_candles`
  and `BinanceExchange.get_candles` exist and are tested, but no script wires them to storage yet.
- No scheduling — this is a one-shot manual CLI run, per [[Open Questions Log#Q28 — Scheduling paradigm for V1|Q28]]
  (still open).
- No Data Quality checks — see [[AI Agent Policy#The only agent approved for V1: Data Quality Agent]].
- Nothing here places trades, backtests, or touches real capital — see [[North Star]].

## Repository layout reference

See [[System Architecture & Repository Layout]] for the full module tree and what each directory
is responsible for.

## Related
- [[Exchange Adapters]]
- [[TimescaleDB Storage]]
- [[Roadmap#Phase 1 — Data Ingestion & Data Quality|Phase 1]]

#athena/setup
