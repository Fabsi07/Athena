# Project Athena

Project Athena is a reproducible quant research platform for discovering,
testing, and validating systematic trading hypotheses on crypto markets.

## What this is

- A data ingestion and storage foundation: exchange adapters, validated
  schemas, and a local TimescaleDB archive.
- The starting point for an iterative research loop (backtesting ↔
  feature engineering ↔ strategy research) built on top of that data.
- A platform designed for skepticism: every result is labeled by stage
  (hypothesis, backtest, out-of-sample, paper trade, live trade), and nothing
  is assumed to generalize.

## What this is not (yet)

- **Not a trading bot.** There is no strategy code, no backtesting engine,
  and no execution logic in this repository yet.
- **Not connected to live trading.** No orders are placed, and no live
  trading will happen until research, validation, paper trading, risk
  controls, and human approval are all in place — see `docs/ROADMAP.md`
  and `docs/PRINCIPLES.md`.
- **Not a distributed system.** Version 1 deliberately skips Kafka/RabbitMQ
  and multi-agent infrastructure in favor of a single local TimescaleDB
  instance. See `AGENTS.md` and `CLAUDE.md` for the reasoning.

## Why data quality first

Every downstream research result is only as trustworthy as the data behind
it. Before any backtest can be believed, the ingestion layer has to
guarantee: no silent data cleaning, explicit UTC timestamps, raw payload
preservation, and idempotent storage. That's what this repository currently
contains, and nothing more.

## Layout

- `backend/data/adapters/` — the `Exchange` abstraction and per-exchange
  implementations (`BybitExchange`, `BinanceExchange`). All external API
  calls live here; nothing else in the codebase is allowed to call an
  exchange API directly.
- `backend/data/schemas.py` — pydantic contracts (`CandleRecord`,
  `FundingRecord`) that every record must pass through before storage.
- `backend/data/storage/` — the TimescaleDB schema and a writer that only
  inserts pre-validated records, idempotently.
- `scripts/` — small CLIs that wire adapters to storage (e.g.
  `ingest_bybit_funding.py`).
- `docs/` — roadmap, architecture, and operating principles.
- `tests/` — schema validation, adapter parsing (mocked HTTP), and storage
  idempotency tests.

## Getting started

```bash
uv sync
uv run pytest

cp .env.example .env
docker compose up -d
uv run python scripts/ingest_bybit_funding.py --symbol BTCUSDT --start 2024-01-01 --end 2024-01-02
```

See `AGENTS.md` and `CLAUDE.md` for the governing rules AI agents and
contributors are expected to follow in this repository.
