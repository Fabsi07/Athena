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
| `timeframe` | `str` | canonical value (`1m/5m/15m/1h/4h/1d`, [[Open Questions Log#Q11 — Canonical timeframe set\|Q11]]) — adapters translate exchange-native interval codes to/from this at the boundary |
| `open_time`, `close_time` | `datetime` (UTC) | candle boundaries |
| `open`, `high`, `low`, `close`, `volume` | `Decimal` | validated non-negative; parsed directly from the exchange's JSON strings to avoid float round-trip precision loss |
| `ingestion_time` | `datetime` (UTC) | when Athena fetched it, not when the candle closed |
| `raw_payload` | `dict \| None` | original exchange JSON, preserved as-is |

## `FundingRecord`

| Field | Type | Notes |
|---|---|---|
| `exchange`, `symbol` | `str` | |
| `funding_timestamp_raw` | `datetime` (UTC) | **exactly as reported by the exchange** |
| `funding_settlement_time` | `datetime` (UTC) | Athena's own interpreted settlement instant |
| `funding_rate` | `Decimal` | |
| `ingestion_time` | `datetime` (UTC) | |
| `raw_payload` | `dict \| None` | |

> [!important] Why raw vs. settlement timestamps are two separate fields
> `funding_timestamp_raw` and `funding_settlement_time` are deliberately kept apart instead of
> collapsed into one value. Collapsing them would bake in an assumption about **when the data was
> actually knowable/tradable** — and that assumption belongs in later, explicit modeling (to avoid
> lookahead bias), not silently in the ingestion layer. For Bybit today the two values happen to be
> identical (Bybit's `fundingRateTimestamp` is documented as the settlement instant itself), but
> the schema doesn't assume that holds for every exchange.

## Resolved decisions reflected in this schema

- [[Open Questions Log#Q10 — Numeric precision for price/volume columns|Q10]] — **resolved:**
  `NUMERIC(28,12)` (not the originally recommended `NUMERIC(20,8)`). Both `CandleRecord`/
  `FundingRecord` (Python `Decimal`) and `schema.sql` (Postgres `NUMERIC(28,12)`) implement this;
  a pre-implementation architecture review had found the committed schema still used
  `DOUBLE PRECISION`/`float`, which has since been fixed.
- [[Open Questions Log#Q11 — Canonical timeframe set|Q11]] — **resolved:** canonical set is
  `1m/5m/15m/1h/4h/1d`, encoded as short strings. `BybitExchange.get_candles()` now takes this
  canonical form as its public parameter and translates internally to Bybit's native interval
  codes (see [[Exchange Adapters]]) — an earlier version stored Bybit's raw codes (`"60"`, `"D"`)
  directly in `timeframe`, which broke cross-exchange joins on the same nominal candle; that's
  fixed now too.

## Related
- [[Exchange Adapter Pattern]]
- [[TimescaleDB Storage]]
- [[Exchange Adapters]]

#athena/data
