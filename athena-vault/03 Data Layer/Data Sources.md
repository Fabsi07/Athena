---
title: Data Sources
tags: [athena, data]
source: CLAUDE.md, AGENTS.md
---

# Data Sources — the $0-Budget Stack

Project Athena prioritizes APIs that are **free and easily interchangeable**. Every source below
must go through an [[Exchange Adapter Pattern|Exchange adapter]] once implemented.

## Approved sources

| Source | Purpose | V1 status |
|---|---|---|
| **Binance** | Live WebSockets, OHLCV, Trades, Orderbook, Klines, Tickers — top priority | ✅ `get_candles` implemented |
| **Bybit** | Funding rates, Open Interest, Orderbook, Klines — core priority | ✅ `get_candles`, `get_funding` implemented |
| **Coinbase** | Baseline for price comparison | ⬜ Not built — scope open, see [[Open Questions Log#Q32 — Coinbase adapter scope\|Q32]] |
| **CoinGecko** | Coins, Marketcap, Volume, Prices, History | ⬜ Not built |
| **FRED** | Macroeconomic data: interest rates, inflation, unemployment, money supply | ⬜ Not built |
| **Alternative.me** | Fear & Greed index | ⬜ Not built |
| **CryptoPanic & RSS** | News, categories, coins, time | ⬜ Not built — staging under debate, see [[Open Questions Log#Q33 — CryptoPanic/RSS staging\|Q33]] |

## Explicitly excluded / deferred

- **X (Twitter):** strictly excluded — cost and API limitations.
- **Glassnode:** approved conceptually, but explicitly deferred to a later iteration, not V1.

## Symbol & timeframe scope (open decision)

The asset/timeframe universe for V1 is **not yet finalized** — see
[[Open Questions Log#Q14 — Asset and timeframe universe for V1|Q14]]. The working recommendation
is to start narrow (BTC, ETH, maybe SOL vs. USDT, on Binance + Bybit) and expand once the pipeline
is proven reliable. Related open question: whether USDT/USDC/BUSD should normalize to a canonical
"USD" or be preserved as distinct quote currencies — see
[[Open Questions Log#Q13 — Canonical symbol/quote-currency convention|Q13]].

## Related
- [[Exchange Adapters]]
- [[Schemas]]
- [[AI Agent Policy#The only agent approved for V1: Data Quality Agent|Data Quality Agent]] — cross-checks Binance vs. Bybit prices using this data

#athena/data
