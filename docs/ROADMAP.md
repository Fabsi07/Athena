# Roadmap

Mirrors the Preferred Development Order in `CLAUDE.md`. Each phase should be
solid — tested, reviewed, and trustworthy — before the next one starts.

## Phase 0 — Project Foundation
Governance docs, directory layout, toolchain (`uv`, `pytest`, Docker Compose
for TimescaleDB). No trading-relevant code.

## Phase 1 — Data Ingestion & Data Quality
Exchange adapters (`Exchange` base class, `BybitExchange`, `BinanceExchange`),
validated schemas, idempotent TimescaleDB storage. A Data Quality Agent that
checks candle completeness, missing values, outliers, and Binance/Bybit
price divergence belongs here once ingestion is stable.

## Phase 2 — Backtesting
A backtesting engine with realistic fills (conservative by default — see
`docs/PRINCIPLES.md`), fees, and slippage, developed alongside feature
engineering and strategy research as one iterative loop.

## Phase 3 — Experiment Tracking
Reproducible experiment records: data version, code version, parameters,
and results, so no backtest result is ever un-reproducible.

## Phase 4 — Paper Trading
Simulated execution against live data, with the same risk controls a live
system would use, before any real capital is at risk.

## Phase 5 — AI Research Assistant
AI assists with hypothesis generation, result summarization, and flaw
identification — never with placing trades or sizing positions from
natural-language confidence.

## Phase 6 — Multi-Agent Research Layer
Multiple agents debating and cross-checking hypotheses. Only pursued once
the single-agent research loop is proven useful.

## Phase 7 — Live Trading
Live trading only after strict validation, paper trading, risk controls, and
explicit human approval. Not started until every prior phase is mature.
