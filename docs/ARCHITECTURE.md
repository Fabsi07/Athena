# Architecture

## Target shape

```
Exchange API -> Exchange Adapter -> validated Records (pydantic) -> TimescaleDB -> idempotent storage
```

Later phases add, in order: Feature Engineering, Backtesting, Experiment
Tracking, Paper Trading, Agents, Live Trading. Each layer only depends on
the layers before it — a backtest never depends on a UI, a strategy never
fetches live data on its own, a research agent never executes trades.

## Exchange Adapters

`backend/data/adapters/base.py` defines the `Exchange` contract:
`get_candles()`, `get_funding()`, `get_orderbook()`, `get_open_interest()`.
Concrete adapters (`BybitExchange`, `BinanceExchange`, and later
`CoinbaseExchange`) implement only what they need for the current phase and
raise `NotImplementedError` for the rest. If an exchange changes its API,
only its adapter file changes — nothing else in the codebase should notice.

No file outside `backend/data/adapters/` is permitted to call an exchange
API directly (the Adapter Mandate in `AGENTS.md`).

## Raw Data Preservation

Every record keeps its exchange's raw JSON payload (`raw_payload`) alongside
the parsed, validated fields. Raw timestamps and interpreted timestamps are
kept as separate fields (see `FundingRecord.funding_timestamp_raw` vs.
`funding_settlement_time`) rather than collapsed into one value — collapsing
them would bake in an assumption about when data was actually knowable, and
that assumption belongs in later, explicit modeling, not in ingestion.

## Historical Database

TimescaleDB, run locally via Docker Compose, pinned to a specific image tag
(never `latest`, for reproducibility). `backend/data/storage/schema.sql`
defines hypertables with primary keys that make repeated ingestion
idempotent (`ON CONFLICT DO NOTHING`). The writer (`timescale_writer.py`)
performs zero transformation — it only accepts records that already passed
`backend/data/schemas.py` validation.

## Feature Engineering / Backtesting / Experiment Tracking / Paper Trading / Agents / Live Trading

Not built yet. Each will get its own top-level directory (`features/`,
`backtesting/`, `strategies/`, `paper_trading/`, `agents/`) per
`AGENTS.md`'s Architecture Principles, kept decoupled from the layers above
and below it.
