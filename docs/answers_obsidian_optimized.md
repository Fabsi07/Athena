---
title: Athena Open Questions — Decision Sheet
source: answers.md
type: decision-log
status: draft
tags: [athena, architecture, decisions, claude-review, obsidian]
created: 2026-07-10
---

# Athena Open Questions — Decision Sheet

> [!info] Purpose
> This note is optimized for Obsidian. Use it to quickly decide whether you accept Claude’s recommendation or write your own answer. The original file contains 34 open implementation questions from `DEVREAD.md`.

## How to use this note

- Tick **Accepted** if you agree with Claude.
- Fill **My decision** only when you want to override or clarify.
- Use **Implementation note** for concrete code/config consequences.
- Questions marked `Later` should not block the current implementation phase.

## Decision overview

| # | Area | Decision topic | Priority | Status |
|---:|---|---|---|---|
| [[#Q01 — Request/Response schema — field types|1]] | `AGENT_PROTOCOL.md` | Request/Response schema — field types | Review | ⬜ Open |
| [[#Q02 — Confidence semantics|2]] | `AGENT_PROTOCOL.md` | Confidence semantics | Review | ⬜ Open |
| [[#Q03 — LLM provider/model|3]] | `AI_ARCHITECTURE.md` | LLM provider/model | Later / Step 7 | ⬜ Open |
| [[#Q04 — V1 agent set|4]] | `AI_ARCHITECTURE.md` | V1 agent set | Later / Step 7 | ⬜ Open |
| [[#Q05 — Transport mechanism for V1|5]] | `API_SPECIFICATION.md` | Transport mechanism for V1 | Decide before implementation | ⬜ Open |
| [[#Q06 — Default fee and slippage values|6]] | `BACKTESTING.md` | Default fee and slippage values | Decide now | ⬜ Open |
| [[#Q07 — Default position sizing model and initial capital|7]] | `BACKTESTING.md` | Default position sizing model and initial capital | Decide now | ⬜ Open |
| [[#Q08 — Overfitting-detection thresholds|8]] | `BACKTESTING.md` | Overfitting-detection thresholds | Decide now | ⬜ Open |
| [[#Q09 — Mandatory benchmark|9]] | `BACKTESTING.md` | Mandatory benchmark | Decide now | ⬜ Open |
| [[#Q10 — Numeric precision for price/volume columns|10]] | `DATABASE_SCHEMA.md` | Numeric precision for price/volume columns | Decide now | ⬜ Open |
| [[#Q11 — Canonical timeframe set|11]] | `DATABASE_SCHEMA.md` | Canonical timeframe set | Decide now | ⬜ Open |
| [[#Q12 — market_sessions default definitions|12]] | `DATABASE_SCHEMA.md` | market_sessions default definitions | Decide now | ⬜ Open |
| [[#Q13 — Canonical symbol/quote-currency convention|13]] | `DATA_ARCHITECTURE.md` | Canonical symbol/quote-currency convention | Decide now | ⬜ Open |
| [[#Q14 — Asset and timeframe universe for V1|14]] | `DATA_ARCHITECTURE.md` | Asset and timeframe universe for V1 | Decide now | ⬜ Open |
| [[#Q15 — Missing-data interpolation trigger mechanism|15]] | `DATA_ARCHITECTURE.md` | Missing-data interpolation trigger mechanism | Decide now | ⬜ Open |
| [[#Q16 — Historical backfill depth|16]] | `DATA_ARCHITECTURE.md` | Historical backfill depth | Decide now | ⬜ Open |
| [[#Q17 — Required V1 feature set and default parameters|17]] | `FEATURE_FACTORY.md` | Required V1 feature set and default parameters | Decide before implementation | ⬜ Open |
| [[#Q18 — Feature version numbering scheme|18]] | `FEATURE_FACTORY.md` | Feature version numbering scheme | Decide before implementation | ⬜ Open |
| [[#Q19 — Logging mechanism and storage target|19]] | `OBSERVABILITY.md` | Logging mechanism and storage target | Decide before implementation | ⬜ Open |
| [[#Q20 — Metrics storage/exposure target|20]] | `OBSERVABILITY.md` | Metrics storage/exposure target | Decide before implementation | ⬜ Open |
| [[#Q21 — Alert delivery channel|21]] | `OBSERVABILITY.md` | Alert delivery channel | Decide before implementation | ⬜ Open |
| [[#Q22 — Default starting virtual capital|22]] | `PAPER_TRADING.md` | Default starting virtual capital | Decide before implementation | ⬜ Open |
| [[#Q23 — "Statistically significant" test/threshold|23]] | `RESEARCH_PROTOCOL.md` | "Statistically significant" test/threshold | Decide now | ⬜ Open |
| [[#Q24 — Train/validation/test split ratios|24]] | `RESEARCH_PROTOCOL.md` | Train/validation/test split ratios | Decide now | ⬜ Open |
| [[#Q25 — Default numeric risk limits|25]] | `RISK_ENGINE.md` | Default numeric risk limits | Decide now | ⬜ Open |
| [[#Q26 — Leverage/margin trading scope|26]] | `RISK_ENGINE.md` | Leverage/margin trading scope | Decide now | ⬜ Open |
| [[#Q27 — Kill-switch trigger thresholds|27]] | `RISK_ENGINE.md` | Kill-switch trigger thresholds | Decide now | ⬜ Open |
| [[#Q28 — Scheduling paradigm for V1|28]] | `SYSTEM_ARCHITECTURE.md` | Scheduling paradigm for V1 | Decide before implementation | ⬜ Open |
| [[#Q29 — Repository layout — binding or illustrative?|29]] | `SYSTEM_ARCHITECTURE.md` | Repository layout — binding or illustrative? | Decide before implementation | ⬜ Open |
| [[#Q30 — Test framework|30]] | `TESTING.md` | Test framework | Decide before implementation | ⬜ Open |
| [[#Q31 — Coverage target|31]] | `TESTING.md` | Coverage target | Decide before implementation | ⬜ Open |
| [[#Q32 — Coinbase adapter scope|32]] | `Cross-document conflicts` | Coinbase adapter scope | Review | ⬜ Open |
| [[#Q33 — CryptoPanic/RSS staging|33]] | `Cross-document conflicts` | CryptoPanic/RSS staging | Later after core pipeline | ⬜ Open |
| [[#Q34 — AGENT_PROTOCOL / AI_ARCHITECTURE staging|34]] | `Cross-document conflicts` | AGENT_PROTOCOL / AI_ARCHITECTURE staging | Later / Step 7 | ⬜ Open |

## Fast path: suggested accepts

> [!success] Practical shortcut
> For a fast V1 implementation, accept most of Claude’s recommendations, but mark Q03, Q04, Q33, and Q34 as deferred/later. Those are scope-control decisions, not current blockers.

## Already implementable

- ✅ `CODING_STANDARDS.md` — no open questions.
- ✅ `PROJECT_RULES.md` — no open questions.

---

## AGENT_PROTOCOL.md

### Q01 — Request/Response schema — field types

**Priority:** `Review`  
**Status:** ⬜ Open

> [!question]- Question
> What concrete data types, formats, and default values should Task ID, Timestamp, Priority, Timeout use?

> [!tip]- Claude recommends
> Task ID = UUID4 string; Timestamp = ISO-8601 UTC; Priority = enum `{LOW, NORMAL, HIGH}` default NORMAL; Timeout = int seconds, default 120s, overridable per task type. Simple and typed, nothing fancy needed.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q02 — Confidence semantics

**Priority:** `Review`  
**Status:** ⬜ Open

> [!question]- Question
> What representation should agent confidence take, and is it self-reported or derived?

> [!tip]- Claude recommends
> Plain float 0.0–1.0, self-reported by the agent. There's no ground truth for research judgments to derive it from, and per CLAUDE.md it must never feed position sizing anyway.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## AI_ARCHITECTURE.md
```

**Implementation note:**

```text

```

---

## AI_ARCHITECTURE.md

### Q03 — LLM provider/model

**Priority:** `Later / Step 7`  
**Status:** ⬜ Open

> [!question]- Question
> Which LLM provider/API (if any) is approved for use, and what is the spend ceiling?

> [!tip]- Claude recommends
> Don't decide this now — it's step 7 work. When it comes up, default to whatever Claude access you already have via your existing subscription (with a hard spend cap) rather than integrating a new vendor.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q04 — V1 agent set

**Priority:** `Later / Step 7`  
**Status:** ⬜ Open

> [!question]- Question
> Which of the six listed agents are actually required for V1 vs. aspirational?

> [!tip]- Claude recommends
> Only the Data Quality Agent — it's the one CLAUDE.md names explicitly as a "good AI use" today. Everything else (Research, Documentation, Code Review, Experiment Review, Architecture Assistant) waits for step 7.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## API_SPECIFICATION.md
```

**Implementation note:**

```text

```

---

## API_SPECIFICATION.md

### Q05 — Transport mechanism for V1

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> Confirm V1 services are plain in-process Python interfaces, and confirm StreamingDataService can be deferred.

> [!tip]- Claude recommends
> Yes to both — in-process Python calls only, no HTTP/gRPC/queues. Defer StreamingDataService entirely until Paper Trading (step 6) actually needs a live feed.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## BACKTESTING.md
```

**Implementation note:**

```text

```

---

## BACKTESTING.md

### Q06 — Default fee and slippage values

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> What are the actual default fee percentages and default fixed slippage value?

> [!tip]- Claude recommends
> ~0.1% taker/maker spot on Binance/Bybit, ~0.05–0.06% taker on perps; flat 5 bps slippage per trade. Always use the taker fee even for "market orders" — conservative per CLAUDE.md's fill-assumption rule.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q07 — Default position sizing model and initial capital

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> Which sizing model is the default, and what's the default starting capital?

> [!tip]- Claude recommends
> "% of Equity" sizing (100% notional per signal, single-asset backtest) with $10,000 starting capital — round number, easy to sanity-check % returns.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q08 — Overfitting-detection thresholds

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> What numeric thresholds should trigger an automatic overfitting warning?

> [!tip]- Claude recommends
> Flag if trade count < 30, annualized Sharpe > 3, or a ±10–20% parameter change swings performance by >50%. Standard quant-research rules of thumb.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q09 — Mandatory benchmark

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> Should every experiment auto-run against a fixed default benchmark, or is it always manual?

> [!tip]- Claude recommends
> Auto-run Buy & Hold (same asset/timeframe) for every experiment by default; anything else is opt-in.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## CODING_STANDARDS.md

No open questions — fully implementable as written.
```

**Implementation note:**

```text

```

---

## DATABASE_SCHEMA.md

### Q10 — Numeric precision for price/volume columns

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> What precision/scale should be used for price and volume columns?

> [!tip]- Claude recommends
> `NUMERIC(20,8)` — standard crypto precision, handles both satoshi-level pricing and large volume figures.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q11 — Canonical timeframe set

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> What is the canonical list of supported timeframes, and how should `timeframe` be encoded?

> [!tip]- Claude recommends
> Start minimal — `1h`, `1d` only, stored as a short string enum. Add `1m`/`5m` later only if a strategy actually needs them, to keep storage/compute small on a $0 budget.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q12 — market_sessions default definitions

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> What are the default UTC time boundaries for the Asia/London/New York sessions?

> [!tip]- Claude recommends
> Asia 00:00–09:00 UTC, London 08:00–16:00 UTC, New York 13:00–21:00 UTC (standard forex session convention).

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## DATA_ARCHITECTURE.md
```

**Implementation note:**

```text

```

---

## DATA_ARCHITECTURE.md

### Q13 — Canonical symbol/quote-currency convention

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> Should USDT/USDC/BUSD normalize to "USD", or should the stablecoin be preserved?

> [!tip]- Claude recommends
> Preserve it — canonical symbol should be `BTC/USDT`, not `BTC/USD`. Stablecoins de-peg sometimes; collapsing them destroys real information and cuts against the data-integrity principle. (This is the one place I'd push back on the doc's own example.)

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q14 — Asset and timeframe universe for V1

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> What specific symbols and timeframes should the V1 collector target?

> [!tip]- Claude recommends
> Start narrow — BTC, ETH (maybe SOL) vs USDT, on Binance + Bybit. Expand once the pipeline is proven reliable.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q15 — Missing-data interpolation trigger mechanism

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> How does a consumer "explicitly request" interpolation?

> [!tip]- Claude recommends
> A simple boolean query parameter (`allow_interpolation=False` by default) rather than a config file or global flag — keeps it obvious at the call site.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q16 — Historical backfill depth

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> How far back should the initial historical backfill go?

> [!tip]- Claude recommends
> Pull the maximum history the free APIs allow (Binance/Bybit klines go back to listing date). Storage is cheap; more history is strictly better for research.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## FEATURE_FACTORY.md
```

**Implementation note:**

```text

```

---

## FEATURE_FACTORY.md

### Q17 — Required V1 feature set and default parameters

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> Which specific features, with which default parameters, must exist in V1?

> [!tip]- Claude recommends
> Keep it small at first — EMA(20/50/200), RSI(14), ATR(14), rolling realized volatility. Enough to support a first simple strategy; grow from there.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q18 — Feature version numbering scheme

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> What format should feature version identifiers take?

> [!tip]- Claude recommends
> Plain incrementing integer (`EMA_v1`, `EMA_v2`) — matches the doc's own examples, no need for semver complexity.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## OBSERVABILITY.md
```

**Implementation note:**

```text

```

---

## OBSERVABILITY.md

### Q19 — Logging mechanism and storage target

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> Where should logs be persisted, and in what format?

> [!tip]- Claude recommends
> Python's standard `logging` module, structured JSON lines, written to local rotating log files — logs are operational, not business data, so they don't belong in the DB.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q20 — Metrics storage/exposure target

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> Should metrics be written to existing System Domain tables, or tracked some other way?

> [!tip]- Claude recommends
> Write into the `system_events` / `data_quality_reports` tables already defined in DATABASE_SCHEMA.md. No separate metrics stack — avoids new infra on a $0 budget.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q21 — Alert delivery channel

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> How should alerts reach the project owner in V1?

> [!tip]- Claude recommends
> ERROR/CRITICAL log entries plus, optionally, a simple SMTP email to yourself. No paid alerting service needed yet.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## PAPER_TRADING.md
```

**Implementation note:**

```text

```

---

## PAPER_TRADING.md

### Q22 — Default starting virtual capital

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> What should the default starting balance be for a new paper trading account?

> [!tip]- Claude recommends
> $10,000, matching the backtest default so results are directly comparable.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## PROJECT_RULES.md

No open questions — fully implementable as written.
```

**Implementation note:**

```text

```

---

## RESEARCH_PROTOCOL.md

### Q23 — "Statistically significant" test/threshold

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> What statistical method and threshold should Athena use?

> [!tip]- Claude recommends
> Bootstrap resampling on trade returns (or a one-sample t-test that mean return > 0), p < 0.05, and a minimum of 30 trades before any significance claim is made at all.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q24 — Train/validation/test split ratios

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> What default split ratios should separate training, validation, and out-of-sample test data?

> [!tip]- Claude recommends
> 60/20/20, split chronologically (never shuffled) — preserves the no-lookahead rule.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## RISK_ENGINE.md
```

**Implementation note:**

```text

```

---

## RISK_ENGINE.md

### Q25 — Default numeric risk limits

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> What are the default limits for max position size, daily loss, drawdown, concurrent positions?

> [!tip]- Claude recommends
> Max 10% of equity per position; max 2% daily loss; max 20% drawdown (triggers a review, not necessarily a hard stop); max 5 concurrent positions. Conservative retail-quant defaults, all overridable per experiment.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q26 — Leverage/margin trading scope

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> Is V1 paper trading spot-only, or does it simulate leveraged perpetual futures?

> [!tip]- Claude recommends
> Spot-only for V1. Funding rate/open interest data gets collected for research features now, but actual leveraged/margin paper trading is a later phase — much simpler risk engine, consistent with "no live trades until mature."

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q27 — Kill-switch trigger thresholds

**Priority:** `Decide now`  
**Status:** ⬜ Open

> [!question]- Question
> What specific thresholds should automatically trigger the kill switch?

> [!tip]- Claude recommends
> Daily loss limit breached, OR max drawdown breached, OR 3+ consecutive execution failures, OR market data feed stale for >5 minutes.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## SYSTEM_ARCHITECTURE.md
```

**Implementation note:**

```text

```

---

## SYSTEM_ARCHITECTURE.md

### Q28 — Scheduling paradigm for V1

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> What scheduling approach should the centralized scheduler use?

> [!tip]- Claude recommends
> In-process (e.g. an asyncio-based loop inside the app), not OS-level cron. Simpler for a single local machine and portable across dev machines.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q29 — Repository layout — binding or illustrative?

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> Is the documented folder layout mandatory, or can it be adapted?

> [!tip]- Claude recommends
> Treat as illustrative. Your current repo (`backend/data/adapters`, etc.) already diverges slightly from the doc's example tree — that's fine as long as each module keeps one clear responsibility.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## TESTING.md
```

**Implementation note:**

```text

```

---

## TESTING.md

### Q30 — Test framework

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> Which Python test framework should be used?

> [!tip]- Claude recommends
> pytest — the de facto Python standard, plays well with your existing `pyproject.toml`.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q31 — Coverage target

**Priority:** `Decide before implementation`  
**Status:** ⬜ Open

> [!question]- Question
> What minimum coverage percentage counts as "high" for critical modules?

> [!tip]- Claude recommends
> 80% overall, 90%+ for Risk Engine and Portfolio Accounting specifically.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text
---

## Cross-document conflicts
```

**Implementation note:**

```text

```

---

## Cross-document conflicts

### Q32 — Coinbase adapter scope

**Priority:** `Review`  
**Status:** ⬜ Open

> [!question]- Question
> Should `CoinbaseExchange` implement the full `ExchangeAdapter` interface, or only a minimal price-lookup method?

> [!tip]- Claude recommends
> Lightweight adapter — just price/ticker lookup for cross-exchange divergence checks. Don't build out orderbook/funding for it; matches CLAUDE.md's "baseline for price comparison" framing, and Coinbase spot doesn't have funding rates anyway.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q33 — CryptoPanic/RSS staging

**Priority:** `Later after core pipeline`  
**Status:** ⬜ Open

> [!question]- Question
> Should CryptoPanic/RSS ingestion be built alongside the exchange/macro adapters now, or deferred?

> [!tip]- Claude recommends
> Defer until the core Binance/Bybit/FRED/CoinGecko/Alternative.me pipeline is solid — matches the literal step-1 list in CLAUDE.md, which omits news sources.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

### Q34 — AGENT_PROTOCOL / AI_ARCHITECTURE staging

**Priority:** `Later / Step 7`  
**Status:** ⬜ Open

> [!question]- Question
> Confirm these two documents describe the eventual step-7 target state only, and are out of scope until data/backtesting/risk/paper-trading are complete.

> [!tip]- Claude recommends
> Confirmed yes — these are step-7 target-state specs only. Nothing to build now.

#### Decision

- [ ] **Accepted** — use Claude’s recommendation as-is
- [ ] **Modified** — use Claude’s recommendation with changes
- [ ] **Rejected** — use a different decision

**My decision:**

```text

```

**Implementation note:**

```text

```

---

## Final decision checklist

- [ ] All `Decide now` questions answered
- [ ] All V1 scope decisions separated from later/step-7 work
- [ ] Accepted recommendations copied into implementation docs/config
- [ ] Overrides documented with a short reason
- [ ] No unresolved blocker remains before coding

## Optional tags

Use these if you split questions into separate notes later:

- `#decision/open`
- `#decision/accepted`
- `#decision/deferred`
- `#athena/v1`
- `#athena/step-7`
