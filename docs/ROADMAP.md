# Roadmap

This roadmap defines the implementation order for Athena. Each phase
must be functionally complete, tested, documented, and reviewed before
the next phase begins.

The architecture is implemented as a **modular monolith** in Version 1
with clearly defined service boundaries. Every module should be designed
so it can later evolve into an independent microservice without changing
its public contracts.

------------------------------------------------------------------------

## Phase 0 --- Project Foundation

-   Repository structure
-   Coding standards
-   Project governance
-   Development environment (`uv`, `pytest`, Docker Compose,
    TimescaleDB)
-   CI-ready project layout
-   Service interfaces and dependency boundaries

No trading logic is implemented during this phase.

------------------------------------------------------------------------

## Phase 1 --- Data Platform

Build the foundation of Athena.

Includes:

-   Exchange adapters (Binance, Bybit, Coinbase reference)
-   Data ingestion
-   TimescaleDB
-   Historical backfill
-   Scheduler
-   Data validation
-   Data Quality Service
-   Collector monitoring
-   Initial Athena Dashboard
-   Logging and observability

Goal:

A reliable, reproducible market data platform.

------------------------------------------------------------------------

## Phase 2 --- Feature Platform & Research

Build reusable research capabilities.

Includes:

-   Feature Factory
-   Feature Registry
-   Feature Versioning
-   Indicator generation
-   Research workflows
-   Dataset versioning

Goal:

Every feature is reproducible and versioned.

------------------------------------------------------------------------

## Phase 3 --- Backtesting & Experiment Tracking

Develop both together.

Includes:

-   Backtesting Engine
-   Portfolio simulation
-   Risk-adjusted metrics
-   Buy & Hold benchmark
-   Experiment tracking
-   Result reproducibility

Goal:

Every experiment can be reproduced exactly.

------------------------------------------------------------------------

## Phase 4 --- Risk Engine & Paper Trading

Includes:

-   Risk Engine
-   Position sizing
-   Kill Switch
-   Portfolio controls
-   Paper Trading
-   Live monitoring
-   Dashboard expansion

Goal:

Operate safely without risking real capital.

------------------------------------------------------------------------

## Phase 5 --- AI Research Assistant

AI augments research only.

Includes:

-   Research Assistant
-   Documentation Assistant
-   Experiment summaries
-   Hypothesis generation
-   Critique support

AI never executes trades, changes risk limits or bypasses human
oversight.

------------------------------------------------------------------------

## Phase 6 --- Multi-Agent Research

Introduce collaborative AI.

Includes:

-   Multi-agent discussions
-   Consensus evaluation
-   Architecture and code review agents
-   Research debate
-   Evidence aggregation

Only after Phase 5 has demonstrated clear value.

------------------------------------------------------------------------

## Phase 7 --- Live Trading

Live trading is the final milestone.

Requirements:

-   Stable data platform
-   Proven backtesting
-   Reliable experiment tracking
-   Validated risk engine
-   Successful paper trading
-   Explicit human approval

Live trading remains optional and must never become the default
operating mode.

------------------------------------------------------------------------

## Long-Term Evolution

Version 1 is implemented as a modular monolith.

As Athena matures, individual bounded contexts may be extracted into
independent microservices without changing business logic or service
contracts.

Potential future services include:

-   Data Service
-   Feature Service
-   Research Service
-   Backtesting Service
-   Risk Service
-   Paper Trading Service
-   AI Service
-   Dashboard/API Gateway

The roadmap prioritizes correctness, reproducibility, and
maintainability over feature velocity.
