---
title: Project Athena Vault
tags: [athena, moc]
---

# Project Athena — Research Vault

> [!info] What this vault is
> A wiki-style knowledge base for **Project Athena**, a $0-budget, reproducible quant research
> platform for discovering and validating systematic crypto trading edges. This vault documents
> the vision, architecture, code that exists today, the rules governing how the project is built,
> and the open decisions still blocking further implementation.
>
> It is generated from the repository's governing docs (`CLAUDE.md`, `AGENTS.md`) and the actual
> code committed so far on `main` (originally built on `athena/v1-data-ingestion`, since merged).
> Treat it as a snapshot — as the codebase evolves, the source files remain the ground truth;
> re-sync this vault when they diverge.

## Where things stand right now

- ✅ **Phase 0 — Foundation** and the start of **Phase 1 — Data Platform** exist in code:
  a Bybit + Binance adapter, pydantic schemas (now `Decimal`-typed, `NUMERIC(28,12)` in Postgres),
  and an idempotent TimescaleDB writer.
- ⬜ Everything from [[Roadmap#Phase 2 — Feature Platform & Research|Feature Platform & Research]]
  onward ([[Roadmap]] phases 2–7) is **not built yet**.
- ✅ 33 of the 34 implementation-blocking ambiguities have been **resolved** by the project owner —
  see [[Open Questions Log]]. Only Q06 (default fee/slippage values) remains explicitly deferred,
  and it blocks [[Roadmap#Phase 3 — Backtesting & Experiment Tracking|Phase 3]].
- 🟡 A pre-implementation architecture review found the roadmap's phase sequencing didn't match
  `CLAUDE.md`/`AGENTS.md`, and that committed code had already drifted from two resolved decisions
  (`NUMERIC(28,12)` precision and canonical timeframe encoding). Both have been fixed; see
  [[Open Questions Log]]'s note on decisions not yet ported into implementation docs for what's
  still outstanding.

## Map of Content

### 01 · Vision
- [[North Star]] — why this project exists, what it should never become
- [[Long-Term Architecture & Development Order]] — the distributed end-state and the mandatory
  build sequence

### 02 · Architecture
- [[System Architecture & Repository Layout]] — current target data flow and module boundaries
- [[Exchange Adapter Pattern]] — the mandatory abstraction layer

### 03 · Data Layer
- [[Data Sources]] — the approved $0-budget data stack
- [[Schemas]] — `CandleRecord` / `FundingRecord` contracts
- [[Exchange Adapters]] — Bybit + Binance, what's implemented today
- [[TimescaleDB Storage]] — schema, idempotency, hypertables

### 04 · Principles
- [[Trading Research Rules]] — bias checklist, fill assumptions, result labeling
- [[Coding Guidelines & Operating Principles]] — modularity, dependency, reproducibility rules

### 05 · AI Agents
- [[AI Agent Policy]] — good vs. bad AI uses, and the Data Quality Agent (the only agent approved
  for V1)

### 06 · Roadmap
- [[Roadmap]] — all 8 phases (0–7), status, and what blocks each one

### 07 · Decisions
- [[Open Questions Log]] — 34 unresolved implementation questions, with recommendations

### 08 · Setup
- [[Getting Started]] — how to run what exists today

### Reference
- [[Glossary]]

## How to use this vault

- Every note links back to the source doc it was derived from (`CLAUDE.md`, `AGENTS.md`,
  `docs/*.md`, or specific code files) — treat those as authoritative if this vault and the repo
  ever disagree.
- Use the **graph view** to see how vision → architecture → data layer → roadmap connect.
- Open [[Open Questions Log]] first if you're about to resume implementation — it's the punch
  list of decisions that need an owner call before more code gets written.

#athena/moc
