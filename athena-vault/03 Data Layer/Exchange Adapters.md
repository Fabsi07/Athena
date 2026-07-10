---
title: Exchange Adapters (Bybit & Binance)
tags: [athena, data, adapters]
source: backend/data/adapters/bybit.py, backend/data/adapters/binance.py
---

# Exchange Adapters — What's Implemented Today

Both adapters implement the [[Exchange Adapter Pattern|`Exchange` contract]]. Neither implements
`get_orderbook()` or `get_open_interest()` yet — both raise `NotImplementedError` explicitly.

## `BybitExchange` (`backend/data/adapters/bybit.py`)

Uses Bybit's V5 REST API (`https://api.bybit.com`), `category="linear"` (perpetuals) by default.

- **`get_candles(symbol, timeframe, start, end)`** — hits `/v5/market/kline`. `timeframe` is the
  **canonical** vocabulary (`1m`, `5m`, `15m`, `1h`, `4h`, `1d` — see
  [[Open Questions Log#Q11 — Canonical timeframe set|Q11]]), translated internally to Bybit's
  native interval codes (`"1"`, `"5"`, `"15"`, `"60"`, `"240"`, `"D"`) for the API call and for the
  close-time-duration lookup; unsupported canonical values raise `ValueError` rather than guessing
  a candle's close time. The returned `CandleRecord.timeframe` carries the canonical value, not
  Bybit's native code — this fixes an earlier version where Bybit rows stored `"60"`/`"D"` while
  Binance rows stored `"1h"`/`"1d"` for the same nominal candle, breaking cross-exchange joins.
- **`get_funding(symbol, start, end)`** — hits `/v5/market/funding/history`.
- **Error handling quirk:** Bybit returns HTTP 200 even on API-level errors, with the real status
  in the JSON body's `retCode` field. The adapter checks both HTTP status *and* `retCode != 0`,
  raising `RuntimeError` on the latter — this is documented in the file precisely because it's an
  easy thing to miss and would otherwise silently swallow real failures.
- Every response row is converted to a [[Schemas|`CandleRecord`/`FundingRecord`]] with the full
  raw row preserved in `raw_payload`.

## `BinanceExchange` (`backend/data/adapters/binance.py`)

Uses Binance's spot REST API (`https://api.binance.com`).

- **`get_candles(symbol, timeframe, start, end)`** only — hits `/api/v3/klines`. Binance's own
  native interval strings already coincide with the canonical vocabulary for `1m/5m/15m/1h/4h/1d`
  (see [[Schemas]]), so no translation layer is needed here the way Bybit's adapter needs one.
- `get_funding`, `get_orderbook`, `get_open_interest` all raise `NotImplementedError` with an
  explicit message ("not implemented in V1").
- Deliberately minimal: the adapter's own docstring says this is *"for later Binance/Bybit price
  cross-checks"* — i.e. it exists to support the [[AI Agent Policy#The only agent approved for V1: Data Quality Agent|Data Quality Agent]], not full Binance trading
  data ingestion yet.

## Shared conventions

- Both adapters accept an optional injected `httpx.Client` (for testability — see
  `tests/test_bybit_adapter.py`, which mocks HTTP with `respx`).
- Both convert exchange millisecond timestamps to timezone-aware UTC `datetime` via a local
  `_ms_to_utc()` helper.
- Both build `open`/`high`/`low`/`close`/`volume`/`funding_rate` as `Decimal`, parsed directly from
  the exchange's JSON string fields (not via `float()`), matching [[Schemas]]'s `NUMERIC(28,12)`
  precision (see [[Open Questions Log#Q10 — Numeric precision for price/volume columns|Q10]]).
- `ingestion_time` is stamped once per API call (`datetime.now(timezone.utc)`), shared across all
  records returned from that call.

## Related
- [[Exchange Adapter Pattern]]
- [[Schemas]]
- [[TimescaleDB Storage]]
- [[Getting Started]] — how to actually run the Bybit funding ingestion script

#athena/data
