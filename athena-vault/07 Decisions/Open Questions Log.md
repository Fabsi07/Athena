---
title: Open Questions Log
tags: [athena, decisions, open-questions]
source: DEVREAD.md, answers.md, docs/answers_obsidian_optimized.md
status: 34 open, 0 accepted
---

# Open Questions Log

34 implementation-blocking ambiguities identified from the original 15-document design spec
(`AGENT_PROTOCOL`, `AI_ARCHITECTURE`, `API_SPECIFICATION`, `BACKTESTING`, `CODING_STANDARDS`,
`DATABASE_SCHEMA`, `DATA_ARCHITECTURE`, `FEATURE_FACTORY`, `OBSERVABILITY`, `PAPER_TRADING`,
`PROJECT_RULES`, `RESEARCH_PROTOCOL`, `RISK_ENGINE`, `SYSTEM_ARCHITECTURE`, `TESTING`), audited
against [[North Star|CLAUDE.md's constraints]] ($0 budget, conservative fills, staged
development). None have an owner decision recorded yet — this is a punch list, not a settled spec.

> [!success] Fast path
> For a fast V1 implementation: accept the recommendation on everything **except** Q03, Q04, Q33,
> Q34 — those four are scope-control decisions (defer to later phases), not current blockers.

> [!info] Already fully implementable, no open questions
> `CODING_STANDARDS.md` and `PROJECT_RULES.md`.

---

## AGENT_PROTOCOL.md

### Q01 — Request/Response schema — field types
**Q:** What concrete data types, formats, and default values should `Task ID`, `Timestamp`,
`Priority`, `Timeout` use?
**Recommendation:** Task ID = UUID4 string; Timestamp = ISO-8601 UTC; Priority = enum
`{LOW, NORMAL, HIGH}` default `NORMAL`; Timeout = int seconds, default 120s, overridable per task
type.

### Q02 — Confidence semantics
**Q:** What representation should agent confidence take, and is it self-reported or derived?
**Recommendation:** Plain float 0.0–1.0, self-reported by the agent — no ground truth exists to
derive it from, and per policy it must never feed position sizing anyway (see
[[AI Agent Policy]]).

---

## AI_ARCHITECTURE.md

### Q03 — LLM provider/model
**Q:** Which LLM provider/API is approved, and what's the spend ceiling?
**Recommendation:** Don't decide now — it's [[Roadmap#Phase 5 — AI Research Assistant|Phase 5]]
work. Default to existing Claude access with a hard spend cap rather than integrating a new
vendor, when the time comes.

### Q04 — V1 agent set
**Q:** Which of the six listed agent types are actually required for V1?
**Recommendation:** Only the [[AI Agent Policy#The only agent approved for V1: Data Quality Agent|Data Quality Agent]].
Everything else waits for Phase 5+.

---

## API_SPECIFICATION.md

### Q05 — Transport mechanism for V1
**Q:** Confirm V1 services are plain in-process Python interfaces, and `StreamingDataService` can
be deferred.
**Recommendation:** Yes to both — in-process Python calls only, no HTTP/gRPC/queues. Defer
`StreamingDataService` until [[Roadmap#Phase 4 — Paper Trading|Paper Trading]] actually needs a
live feed.

---

## BACKTESTING.md

### Q06 — Default fee and slippage values
**Q:** What are the actual default fee percentages and slippage value?
**Recommendation:** ~0.1% taker/maker spot on Binance/Bybit, ~0.05–0.06% taker on perps; flat 5 bps
slippage per trade. Always use the taker fee even for "market orders" — conservative per
[[Trading Research Rules]].

### Q07 — Default position sizing model and initial capital
**Q:** Which sizing model is the default, and what's the default starting capital?
**Recommendation:** "% of Equity" sizing (100% notional per signal, single-asset backtest), $10,000
starting capital.

### Q08 — Overfitting-detection thresholds
**Q:** What numeric thresholds should trigger an automatic overfitting warning?
**Recommendation:** Flag if trade count < 30, annualized Sharpe > 3, or a ±10–20% parameter change
swings performance by >50%.

### Q09 — Mandatory benchmark
**Q:** Should every experiment auto-run against a fixed benchmark, or is it manual?
**Recommendation:** Auto-run Buy & Hold (same asset/timeframe) by default; anything else opt-in.

---

## CODING_STANDARDS.md

No open questions — fully implementable as written.

---

## DATABASE_SCHEMA.md

### Q10 — Numeric precision for price/volume columns
**Q:** What precision/scale should price and volume columns use?
**Recommendation:** `NUMERIC(20,8)`. Note: current code ([[Schemas]], [[TimescaleDB Storage]])
actually uses `float` / `DOUBLE PRECISION` — **not yet reconciled with this recommendation.**

### Q11 — Canonical timeframe set
**Q:** What is the canonical list of supported timeframes, and how is `timeframe` encoded?
**Recommendation:** Start minimal — `1h`, `1d` only, short string enum. Add `1m`/`5m` later only if
a strategy needs them. Note: [[Exchange Adapters]] currently validate against each exchange's own
native interval strings, not a canonical set.

### Q12 — market_sessions default definitions
**Q:** What are the default UTC boundaries for Asia/London/New York sessions?
**Recommendation:** Asia 00:00–09:00 UTC, London 08:00–16:00 UTC, New York 13:00–21:00 UTC
(standard forex convention).

---

## DATA_ARCHITECTURE.md

### Q13 — Canonical symbol/quote-currency convention
**Q:** Should USDT/USDC/BUSD normalize to "USD", or be preserved as distinct?
**Recommendation:** Preserve it — canonical symbol should be `BTC/USDT`, not `BTC/USD`. Stablecoins
de-peg sometimes; collapsing them destroys real information.

### Q14 — Asset and timeframe universe for V1
**Q:** What specific symbols and timeframes should the V1 collector target?
**Recommendation:** Start narrow — BTC, ETH (maybe SOL) vs USDT, on Binance + Bybit.

### Q15 — Missing-data interpolation trigger mechanism
**Q:** How does a consumer "explicitly request" interpolation?
**Recommendation:** A boolean query parameter (`allow_interpolation=False` by default).

### Q16 — Historical backfill depth
**Q:** How far back should the initial historical backfill go?
**Recommendation:** Pull the maximum history the free APIs allow.

---

## FEATURE_FACTORY.md

### Q17 — Required V1 feature set and default parameters
**Q:** Which specific features, with which default parameters, must exist in V1?
**Recommendation:** EMA(20/50/200), RSI(14), ATR(14), rolling realized volatility.

### Q18 — Feature version numbering scheme
**Q:** What format should feature version identifiers take?
**Recommendation:** Plain incrementing integer (`EMA_v1`, `EMA_v2`).

---

## OBSERVABILITY.md

### Q19 — Logging mechanism and storage target
**Q:** Where should logs be persisted, and in what format?
**Recommendation:** Python's standard `logging` module, structured JSON lines, local rotating log
files.

### Q20 — Metrics storage/exposure target
**Q:** Should metrics go into existing System Domain tables, or elsewhere?
**Recommendation:** Write into `system_events` / `data_quality_reports` tables. No separate metrics
stack — avoids new infra on a $0 budget.

### Q21 — Alert delivery channel
**Q:** How should alerts reach the project owner in V1?
**Recommendation:** ERROR/CRITICAL log entries, optionally a simple SMTP email.

---

## PAPER_TRADING.md

### Q22 — Default starting virtual capital
**Q:** What should the default starting balance be for a new paper trading account?
**Recommendation:** $10,000, matching the backtest default (Q07) for direct comparability.

---

## PROJECT_RULES.md

No open questions — fully implementable as written.

---

## RESEARCH_PROTOCOL.md

### Q23 — "Statistically significant" test/threshold
**Q:** What statistical method and threshold should Athena use?
**Recommendation:** Bootstrap resampling on trade returns (or one-sample t-test that mean return >
0), p < 0.05, minimum 30 trades before any significance claim.

### Q24 — Train/validation/test split ratios
**Q:** What default split ratios separate training, validation, and out-of-sample test data?
**Recommendation:** 60/20/20, split chronologically (never shuffled) — preserves the no-lookahead
rule.

---

## RISK_ENGINE.md

### Q25 — Default numeric risk limits
**Q:** What are the default limits for max position size, daily loss, drawdown, concurrent
positions?
**Recommendation:** Max 10% of equity per position; max 2% daily loss; max 20% drawdown (triggers
review, not a hard stop); max 5 concurrent positions.

### Q26 — Leverage/margin trading scope
**Q:** Is V1 paper trading spot-only, or does it simulate leveraged perpetual futures?
**Recommendation:** Spot-only for V1. Funding/open-interest data is still collected for research
features now, but leveraged paper trading is a later phase.

### Q27 — Kill-switch trigger thresholds
**Q:** What thresholds should automatically trigger the kill switch?
**Recommendation:** Daily loss limit breached, OR max drawdown breached, OR 3+ consecutive
execution failures, OR market data feed stale for >5 minutes.

---

## SYSTEM_ARCHITECTURE.md

### Q28 — Scheduling paradigm for V1
**Q:** What scheduling approach should the centralized scheduler use?
**Recommendation:** In-process (e.g. asyncio loop), not OS-level cron.

### Q29 — Repository layout — binding or illustrative?
**Q:** Is the documented folder layout mandatory, or adaptable?
**Recommendation:** Illustrative — see [[System Architecture & Repository Layout]]; the real repo
already diverges slightly and that's fine as long as module responsibilities stay separated.

---

## TESTING.md

### Q30 — Test framework
**Q:** Which Python test framework should be used?
**Recommendation:** pytest — already in use, see [[Coding Guidelines & Operating Principles]].

### Q31 — Coverage target
**Q:** What minimum coverage percentage counts as "high" for critical modules?
**Recommendation:** 80% overall, 90%+ for Risk Engine and Portfolio Accounting specifically.

---

## Cross-document conflicts

### Q32 — Coinbase adapter scope
**Q:** Should `CoinbaseExchange` implement the full `ExchangeAdapter` interface, or just a minimal
price-lookup method?
**Conflict:** `CLAUDE.md` frames Coinbase as "baseline for price comparison"; other docs list it as
a full market-data source.
**Recommendation:** Lightweight adapter — price/ticker lookup only, for cross-exchange divergence
checks. Coinbase spot doesn't have funding rates anyway.

### Q33 — CryptoPanic/RSS staging
**Q:** Should CryptoPanic/RSS ingestion be built alongside the exchange/macro adapters now, or
deferred?
**Conflict:** `CLAUDE.md`'s Version 1 Data Strategy lists it as in-scope; its own Preferred
Development Order step 1 omits news sources.
**Recommendation:** Defer until the core Binance/Bybit/FRED/CoinGecko/Alternative.me pipeline is
solid.

### Q34 — AGENT_PROTOCOL / AI_ARCHITECTURE staging
**Q:** Confirm these describe eventual step-7 target state only, out of scope until data/
backtesting/risk/paper-trading are complete.
**Recommendation:** Confirmed — target-state specs only. Nothing to build now. See
[[Long-Term Architecture & Development Order#Preferred development order]].

---

## Final decision checklist

- [ ] All "decide now" questions answered by the project owner
- [ ] V1 scope decisions separated from later/Phase-5+ work
- [ ] Accepted recommendations copied into actual implementation docs/config
- [ ] Overrides documented with a short reason
- [ ] No unresolved blocker remains before the next round of coding

## Related
- [[Roadmap]]
- [[Trading Research Rules]]
- [[Schemas]]

#athena/decisions
