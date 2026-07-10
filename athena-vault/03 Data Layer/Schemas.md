---
title: Schemas
tags: [athena, data, schemas]
source: backend/data/schemas.py
---

# Schemas — Typed Contracts for Market Data

> [!quote] From `backend/data/schemas.py`
> Every record stored to TimescaleDB must pass through one of these models first. No
> transformation logic lives downstream of validation here.

Both models are pydantic `BaseModel`s. Every datetime field is validated to be **timezone-aware
and normalized to UTC** — naive datetimes or non-UTC offsets raise a `ValueError` at construction
time, not later at storage time.

## `CandleRecord`

| Field | Type | Notes |
|---|---|---|
| `exchange` | `str` | e.g. `"bybit"`, `"binance"` |
| `symbol` | `str` | exchange-native symbol, e.g. `"BTCUSDT"` |
| `timeframe` | `str` | exchange-native interval string (not yet a canonical enum — see [[Open Questions Log#Q11 — Canonical timeframe set\|Q11]]) |
| `open_time`, `close_time` | `datetime` (UTC) | candle boundaries |
| `open`, `high`, `low`, `close`, `volume` | `float` | validated non-negative |
| `ingestion_time` | `datetime` (UTC) | when Athena fetched it, not when the candle closed |
| `raw_payload` | `dict \| None` | original exchange JSON, preserved as-is |

## `FundingRecord`

| Field | Type | Notes |
|---|---|---|
| `exchange`, `symbol` | `str` | |
| `funding_timestamp_raw` | `datetime` (UTC) | **exactly as reported by the exchange** |
| `funding_settlement_time` | `datetime` (UTC) | Athena's own interpreted settlement instant |
| `funding_rate` | `float` | |
| `ingestion_time` | `datetime` (UTC) | |
| `raw_payload` | `dict \| None` | |

> [!important] Why raw vs. settlement timestamps are two separate fields
> `funding_timestamp_raw` and `funding_settlement_time` are deliberately kept apart instead of
> collapsed into one value. Collapsing them would bake in an assumption about **when the data was
> actually knowable/tradable** — and that assumption belongs in later, explicit modeling (to avoid
> lookahead bias), not silently in the ingestion layer. For Bybit today the two values happen to be
> identical (Bybit's `fundingRateTimestamp` is documented as the settlement instant itself), but
> the schema doesn't assume that holds for every exchange.

## Open questions affecting this schema

- [[Open Questions Log#Q10 — Numeric precision for price/volume columns|Q10]] — current code uses
  Python `float` / Postgres `DOUBLE PRECISION`; the DB design doc originally called for
  `NUMERIC(20,8)` fixed-point precision. Not yet reconciled.
- [[Open Questions Log#Q11 — Canonical timeframe set|Q11]] — no enum of supported timeframes exists
  yet; adapters currently validate against their own exchange-specific interval maps (see
  [[Exchange Adapters]]).

## Related
- [[Exchange Adapter Pattern]]
- [[TimescaleDB Storage]]
- [[Exchange Adapters]]

#athena/data
