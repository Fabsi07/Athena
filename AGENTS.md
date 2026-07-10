# AGENTS.md

## Project North Star

Project Athena is a reproducible quant research platform for discovering, testing, and validating trading hypotheses.

The goal is not to rush toward a live trading bot. The goal is to build a durable research system that can:

- collect reliable market data,
- run realistic backtests,
- track every experiment,
- compare strategies against benchmarks,
- reject weak ideas quickly,
- promote only validated candidates to paper trading,
- and eventually support agent-assisted research.

Treat "autonomous multi-agent trading AI" as the long-term vision, not the first implementation milestone.

## Current Build Philosophy

Prefer a lean research platform before complex AI automation and before heavy DevOps infrastructure.

The target system architecture is modeled as: **WebSocket** $\rightarrow$ **Kafka / RabbitMQ** $\rightarrow$ **Collector** $\rightarrow$ **TimescaleDB** $\rightarrow$ **Feature Store** $\rightarrow$ **Research Layer**. 

However, for Version 1, do not introduce message brokers (Kafka/RabbitMQ). Stick to direct ingestion into a local database (TimescaleDB) and build in the following order, matching `docs/ROADMAP.md` (the authoritative implementation order):

0. **Project Foundation** — repository structure, coding standards, governance, dev environment, service interfaces. No trading logic.
1. **Data Platform** — exchange adapters, data ingestion, TimescaleDB, historical backfill, scheduler, data validation, Data Quality Service, collector monitoring, initial dashboard, logging/observability. Save everything from Day 1.
2. **Feature Platform & Research** — Feature Factory, Feature Registry, feature versioning, indicator generation, research workflows, dataset versioning.
3. **Backtesting & Experiment Tracking** — developed together: backtesting engine, portfolio simulation, risk-adjusted metrics, Buy & Hold benchmark, experiment tracking, result reproducibility.
4. **Risk Engine & Paper Trading** — risk engine, position sizing, kill switch, portfolio controls, paper trading, live monitoring, dashboard expansion.
5. **AI Research Assistant** — research assistant, documentation assistant, experiment summaries, hypothesis generation, critique support.
6. **Multi-Agent Research** — multi-agent discussions, consensus evaluation, architecture/code review agents, research debate, evidence aggregation. Only after Phase 5 has demonstrated clear value.
7. **Live Trading** — only after strict validation, a validated risk engine, successful paper trading, and explicit human approval.

If there is a conflict between building something impressive and building something measurable, choose measurable. 

## Agent Behavior

When working in this repository:

- Read the existing project structure before making changes.
- Keep changes small, testable, and reversible.
- Do not introduce a large framework unless the project clearly needs it.
- Prefer simple modules with explicit data contracts.
- Keep trading logic separate from execution logic.
- Keep research code separate from live-trading code.
- Never let an AI-generated signal trade real funds directly.
- Assume financial backtests are fragile until proven otherwise.
- Watch aggressively for lookahead bias, survivorship bias, data snooping, and overfitting.
- Default fill assumptions must be conservative. Market orders cross the spread and include fees/slippage. Limit-order fill-at-touch is optimistic and may only be used when explicitly labeled and justified.

## Architecture Principles

Use clear boundaries between these areas:

- `backend/data/`: collectors, normalization, storage adapters.
- `research/`: notebooks, experiments, hypotheses, exploratory scripts.
- `backtesting/`: strategy simulation, cost models, metrics, validation.
- `features/`: feature generation and feature validation.
- `strategies/`: strategy definitions and parameter sets.
- `risk/`: risk engine, position sizing, kill switch, portfolio risk controls — independent of strategy code, with final authority over position sizing and execution approval.
- `paper_trading/`: simulated live trading against real-time data.
- `agents/`: AI-assisted analysis, critique, summarization, and research workflows.
- `docs/`: design notes, assumptions, experiment summaries, and operating rules.

Do not couple these layers casually. A backtest should not depend on a UI. A strategy should not secretly fetch live data. A research agent should not execute trades.

## Data Rules & The Adapter Mandate

Market data is the foundation of the system. We prioritize APIs that are free and easily interchangeable. 

**Direct API calls within strategy or research code are strictly forbidden.** All external data must pass through a strict `Exchange` abstraction layer.

- The base `Exchange` class must define explicit contracts such as `get_candles()`, `get_orderbook()`, `get_funding()`, and `get_open_interest()`.
- Exchange-specific implementations (e.g., `BinanceExchange`, `BybitExchange`, `CoinbaseExchange`) must inherit from this class.
- If an exchange changes its API, only that specific adapter file should change, protecting the rest of the project codebase.

Agents must:

- preserve raw data where possible,
- record data source, symbol, timeframe, timestamp, and ingestion time,
- normalize timestamps explicitly to UTC,
- avoid silently filling missing data,
- make data cleaning decisions visible,
- store enough metadata to reproduce an experiment later.

### Approved Data Sources
- **Binance:** Top priority for OHLCV, Live WebSockets, Trades, Orderbook, Klines, and Tickers.
- **Bybit:** Core priority for Funding, Open Interest, Orderbook, and Klines.
- **Coinbase:** Approved for price comparison.
- **News:** CryptoPanic (News, categories, coins, time) and crawling RSS feeds.
- **Sentiment:** Alternative.me for Fear & Greed indices.
- **Macroeconomics:** FRED for Interest Rates, Inflation, Unemployment Rate, and Money Supply.
- **On-Chain/Reference:** CoinGecko (Coins, Marketcap, Volume, Prices, History). Glassnode is approved for later phases.
- **Strictly Excluded:** X (Twitter) API is excluded for now due to cost and limitations.

## AI and Agent Rules

AI agents must not place live trades, bypass human approval, hide uncertainty, invent data, or claim edge without statistical support.

**Exception for Version 1:** The only permitted early-stage AI agent is a **"Data Quality Agent"**. Its job is exclusively to monitor data integrity and alert on issues. 
The Data Quality Agent must rigorously verify:
- Are candles complete?
- Are there missing values or outliers?
- Do prices align approximately between Binance and Bybit?
- Have WebSocket connections failed?
- Were duplicate records stored?

If implementing agents, use structured outputs:

```text
agent_name:
hypothesis:
input_data:
signal:
confidence:
evidence:
counterarguments:
known_limitations:
recommended_next_test: