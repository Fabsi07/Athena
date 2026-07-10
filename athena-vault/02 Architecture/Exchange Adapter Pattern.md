---
title: Exchange Adapter Pattern
tags: [athena, architecture, mandatory-pattern]
source: AGENTS.md, backend/data/adapters/base.py
---

# Exchange Adapter Pattern (the Adapter Mandate)

> [!danger] Non-negotiable rule
> **Direct API calls within strategy or research code are strictly forbidden.** All external data
> must pass through a strict `Exchange` abstraction layer. No file outside
> `backend/data/adapters/` is permitted to call an exchange API directly.

## Why

If an exchange changes its API, only that specific adapter file should change — protecting the
rest of the codebase. This is the single most enforced architectural rule in the project.

## The contract (`backend/data/adapters/base.py`)

```python
class Exchange(ABC):
    @abstractmethod
    def get_candles(self, symbol, timeframe, start, end) -> list[CandleRecord]: ...

    @abstractmethod
    def get_funding(self, symbol, start, end) -> list[FundingRecord]: ...

    @abstractmethod
    def get_orderbook(self, symbol): ...

    @abstractmethod
    def get_open_interest(self, symbol, start, end): ...
```

Concrete adapters implement only what they need for the current phase and **raise
`NotImplementedError`** for the rest, loudly, rather than silently returning empty data. See
[[Exchange Adapters]] for what `BybitExchange` and `BinanceExchange` actually implement today.

## Rules for agents/contributors working with data

- Preserve raw data where possible (`raw_payload` field on every record).
- Record data source, symbol, timeframe, timestamp, and ingestion time.
- Normalize timestamps explicitly to UTC — naive or non-UTC datetimes are rejected by
  [[Schemas]]'s validators, not silently coerced.
- Avoid silently filling missing data.
- Make data-cleaning decisions visible (in reviewable code, not implicit transforms).
- Store enough metadata to reproduce an experiment later.

## Planned subclasses

| Adapter | Status | Scope |
|---|---|---|
| `BybitExchange` | ✅ Implemented | `get_candles`, `get_funding`. `get_orderbook`/`get_open_interest` raise `NotImplementedError` |
| `BinanceExchange` | ✅ Implemented | `get_candles` only — deliberately minimal, for Binance/Bybit price cross-checks (see [[AI Agent Policy#The only agent approved for V1: Data Quality Agent\|Data Quality Agent]]) |
| `CoinbaseExchange` | ⬜ Not built | Scope under debate — see [[Open Questions Log#Q32 — Coinbase adapter scope|Q32]]: full adapter vs. lightweight price-lookup only |

## Related
- [[System Architecture & Repository Layout]]
- [[Exchange Adapters]]
- [[Schemas]]

#athena/architecture
