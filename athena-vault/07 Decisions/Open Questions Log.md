---
title: Open Questions Log
tags: [athena, decisions, open-questions]
source: DEVREAD.md, answers.md, docs/answers_obsidian_optimized.md
status: 33 resolved (accepted or modified), 1 explicitly deferred (Q06)
---

# Open Questions Log

34 implementation-blocking ambiguities identified from the original 15-document design spec
(`AGENT_PROTOCOL`, `AI_ARCHITECTURE`, `API_SPECIFICATION`, `BACKTESTING`, `CODING_STANDARDS`,
`DATABASE_SCHEMA`, `DATA_ARCHITECTURE`, `FEATURE_FACTORY`, `OBSERVABILITY`, `PAPER_TRADING`,
`PROJECT_RULES`, `RESEARCH_PROTOCOL`, `RISK_ENGINE`, `SYSTEM_ARCHITECTURE`, `TESTING`), audited
against [[North Star|CLAUDE.md's constraints]] ($0 budget, conservative fills, staged
development).

> [!success] Resolved
> `docs/answers_obsidian_optimized.md` is the **authoritative decision log** — the project owner
> has recorded a decision for every question except Q06, which is explicitly deferred ("decide
> later" — see below). Each entry below shows the actual decision, not just the original
> recommendation; where the owner modified Claude's recommendation, that's called out.

> [!info] Already fully implementable, no open questions
> `CODING_STANDARDS.md` and `PROJECT_RULES.md`.

> [!warning] Not yet ported into implementation docs
> These decisions currently live only in `docs/answers_obsidian_optimized.md` — most of the
> referenced source documents (`DATABASE_SCHEMA.md`, `RISK_ENGINE.md`, `BACKTESTING.md`, etc.)
> don't exist anywhere in the repo (`DEVREAD.md` traces them to an external, uncommitted design-doc
> bundle). A pre-implementation architecture review flagged this as the root cause of two concrete
> bugs that had already crept into committed code (Q10, Q11 below) and recommended giving these
> decisions a real home in `docs/`. That porting work is still open.

---

## AGENT_PROTOCOL.md

### Q01 — Request/Response schema — field types
**Q:** What concrete data types, formats, and default values should `Task ID`, `Timestamp`,
`Priority`, `Timeout` use?
**Decision (modified):** Task ID = UUID4 string, immutable. Timestamp = ISO-8601 UTC. Priority =
enum `{LOW, NORMAL, HIGH, CRITICAL}` (owner added `CRITICAL` to Claude's original 3-value enum),
default `NORMAL`. Timeout = int seconds, default 120, `null` = no timeout, overridable per task
type. Also added: optional UUID4 `Correlation ID` for tracing related requests, and an optional
`Metadata` dict for future extension. All request metadata is immutable after task creation.

### Q02 — Confidence semantics
**Q:** What representation should agent confidence take, and is it self-reported or derived?
**Decision (modified):** Agent Confidence = self-reported float 0.0–1.0 (matches Claude's
recommendation). Owner additionally specified a System Confidence concept — optionally derivable
later from multi-agent agreement, data quality, or statistical significance — not calculated in
V1. Either way, confidence never feeds position sizing, execution, or risk limits; see
[[AI Agent Policy]].

---

## AI_ARCHITECTURE.md

### Q03 — LLM provider/model
**Q:** Which LLM provider/API is approved, and what's the spend ceiling?
**Decision (modified):** No provider required for V1 (disabled by default). Athena must stay
provider-agnostic — provider, model, endpoint, token budget, and timeout are all configurable, and
no business logic may depend on a specific provider. Hard monthly spend limit defaults to $0; paid
providers require explicit opt-in. Local models preferred when sufficient. This is broader than
Claude's original recommendation (which assumed reusing an existing Claude subscription).

### Q04 — V1 agent set
**Q:** Which of the six listed agent types are actually required for V1?
**Decision (modified):** [[AI Agent Policy#The only agent approved for V1: Data Quality Agent|Data
Quality Agent]] only, as recommended. Owner additionally carved out a Documentation Agent as
experimental/optional (may be enabled manually, not part of the operational platform). Everything
else (Research, Experiment Review, Code Review, Architecture Assistant, Multi-Agent Coordinator) is
deferred to [[Roadmap#Phase 5 — AI Research Assistant|Phase 5]]+.

---

## API_SPECIFICATION.md

### Q05 — Transport mechanism for V1
**Q:** Confirm V1 services are plain in-process Python interfaces, and `StreamingDataService` can
be deferred.
**Decision (accepted as recommended):** Yes to both — in-process Python calls only, no
HTTP/gRPC/queues. `StreamingDataService` deferred until
[[Roadmap#Phase 4 — Risk Engine & Paper Trading|Paper Trading]] actually needs a live feed.

---

## BACKTESTING.md

### Q06 — Default fee and slippage values
**Q:** What are the actual default fee percentages and slippage value?
**Decision:** ⬜ **Explicitly deferred by the project owner** — "we can't answer it now, it's
better to decide later." This is the one question still genuinely open. Since
`docs/PRINCIPLES.md` requires fees, slippage, and conservative fill assumptions in every backtest,
this is a real blocker for [[Roadmap#Phase 3 — Backtesting & Experiment Tracking|Phase 3]], not
just an unanswered nice-to-have.

### Q07 — Default position sizing model and initial capital
**Q:** Which sizing model is the default, and what's the default starting capital?
**Decision (modified):** Fixed 5% of portfolio equity per position (owner chose 5%, not Claude's
recommended 100%-notional single-asset sizing), $10,000 USDT starting capital. Strategies may
optionally propose a size/allocation, but the Risk Engine always has final authority to approve,
reduce, reject, or rebalance it.

### Q08 — Overfitting-detection thresholds
**Q:** What numeric thresholds should trigger an automatic overfitting warning?
**Decision (modified):** Same numeric thresholds as recommended (trade count < 30, annualized
Sharpe > 3.0, ±10–20% parameter change swinging performance >50%), plus two added conditions:
strong in-sample/out-of-sample divergence, and large walk-forward degradation. All configurable,
and explicitly **warnings only** — they must never auto-reject a strategy; final call stays with
the researcher.

### Q09 — Mandatory benchmark
**Q:** Should every experiment auto-run against a fixed benchmark, or is it manual?
**Decision (accepted as recommended):** Auto-run Buy & Hold (same asset/timeframe) by default;
anything else opt-in.

---

## CODING_STANDARDS.md

No open questions — fully implementable as written.

---

## DATABASE_SCHEMA.md

### Q10 — Numeric precision for price/volume columns
**Q:** What precision/scale should price and volume columns use?
**Decision (modified):** `NUMERIC(28,12)` — higher precision than Claude's recommended
`NUMERIC(20,8)`, with room to increase further if a future exchange needs it. **Implemented**: both
`schema.sql` and `CandleRecord`/`FundingRecord` (via Python `Decimal`) now use this — see
[[Schemas]] and [[TimescaleDB Storage]]. A pre-implementation architecture review had found the
committed code still used `DOUBLE PRECISION`/`float` despite this decision; that drift is fixed.

### Q11 — Canonical timeframe set
**Q:** What is the canonical list of supported timeframes, and how is `timeframe` encoded?
**Decision (modified):** Full set `1m, 5m, 15m, 1h, 4h, 1d`, encoded as short strings — broader
than Claude's "start with just 1h/1d" recommendation; the architecture supports the whole set from
the start even though collectors may initially fetch only a subset (see Q14). **Implemented**:
[[Exchange Adapters]] now translate exchange-native interval codes to/from this canonical set at
the adapter boundary. A pre-implementation architecture review had found Bybit's adapter storing
its own native codes (`"60"`, `"D"`) directly, which silently broke cross-exchange joins on the
same nominal candle; that's fixed.

### Q12 — market_sessions default definitions
**Q:** What are the default UTC boundaries for Asia/London/New York sessions?
**Decision (modified):** Asia 00:00–08:00 UTC (not 00:00–09:00 as recommended), London 08:00–16:00
UTC, New York 13:00–21:00 UTC. Explicitly analytical time windows only, not exchange open/close
times; configurable, with DST support possible later.

---

## DATA_ARCHITECTURE.md

### Q13 — Canonical symbol/quote-currency convention
**Q:** Should USDT/USDC/BUSD normalize to "USD", or be preserved as distinct?
**Decision (accepted as recommended):** Preserve it — canonical symbol is `BTC/USDT`, not
`BTC/USD`. Stablecoins de-peg sometimes; collapsing them destroys real information.
**Not yet implemented**: both adapters currently store the exchange's raw symbol format
(`"BTCUSDT"`, no separator) rather than this canonical form — flagged in the architecture review
as a remaining gap, not yet actioned.

### Q14 — Asset and timeframe universe for V1
**Q:** What specific symbols and timeframes should the V1 collector target?
**Decision (modified):** BTC/USDT and ETH/USDT on Binance + Bybit (Coinbase as reference/price-check
only) — narrower than Claude's "maybe add SOL" suggestion. Full canonical timeframe set is
supported architecturally (Q11), but initial collection is scoped to `1h`/`1d` only; lower
timeframes and additional assets (SOL, BNB, XRP, ...) come later, once the pipeline proves stable.

### Q15 — Missing-data interpolation trigger mechanism
**Q:** How does a consumer "explicitly request" interpolation?
**Decision (modified):** Not a boolean flag as recommended — an explicit
`missing_data_policy` parameter with four supported values: `none` (default), `linear`,
`forward_fill`, `backward_fill`. Every experiment must record which policy was used, for
reproducibility.

### Q16 — Historical backfill depth
**Q:** How far back should the initial historical backfill go?
**Decision (accepted as recommended):** Pull the maximum history the free APIs allow.

---

## FEATURE_FACTORY.md

### Q17 — Required V1 feature set and default parameters
**Q:** Which specific features, with which default parameters, must exist in V1?
**Decision (modified):** Larger set than recommended — Trend: EMA(20/50/200), SMA(20/50).
Momentum: RSI(14), MACD(12,26,9). Volatility: ATR(14), Bollinger Bands(20,2), rolling realized
volatility(20). Volume: VWAP. All defaults configurable; every feature version registered in the
Feature Registry (e.g. `EMA20_v1` → `EMA20_v2` on any implementation/parameter change).

### Q18 — Feature version numbering scheme
**Q:** What format should feature version identifiers take?
**Decision (accepted as recommended):** Plain incrementing integer (`EMA20_v1`, `EMA20_v2`).

---

## OBSERVABILITY.md

### Q19 — Logging mechanism and storage target
**Q:** Where should logs be persisted, and in what format?
**Decision (accepted as recommended):** Python's standard `logging` module, structured JSON lines,
local rotating log files.

### Q20 — Metrics storage/exposure target
**Q:** Should metrics go into existing System Domain tables, or elsewhere?
**Decision (modified):** System metrics → `system_events`; data-quality metrics →
`data_quality_reports` (as recommended, no separate metrics stack). Owner added an explicit
ownership rule: metrics are owned by the service that produces them, the dashboard aggregates
through service interfaces, and no service may directly access another service's internal
database. Research/experiment metrics (Sharpe, Sortino, Max Drawdown, CAGR, Profit Factor) belong
exclusively to experiment records, never duplicated as operational metrics.

### Q21 — Alert delivery channel
**Q:** How should alerts reach the project owner in V1?
**Decision (modified):** Broader than the recommended "log entries + optional email" — Athena gets
an **internal dashboard from V1**, growing across versions. V1 dashboard: collector status, DB
status, active collectors, ingestion rate, API health, missing candles, data-quality overview,
running experiments, backtest progress, recent logs, CPU/memory/disk. No dedicated metrics stack
(Prometheus/Grafana/OpenTelemetry) in V1; the dashboard reads from the existing DB and logs.

---

## PAPER_TRADING.md

### Q22 — Default starting virtual capital
**Q:** What should the default starting balance be for a new paper trading account?
**Decision (accepted as recommended):** $10,000, matching the backtest default (Q07) for direct
comparability.

---

## PROJECT_RULES.md

No open questions — fully implementable as written.

---

## RESEARCH_PROTOCOL.md

### Q23 — "Statistically significant" test/threshold
**Q:** What statistical method and threshold should Athena use?
**Decision (modified):** Bootstrap resampling on trade returns as the V1 default (as recommended),
95% confidence, p < 0.05, minimum 30 trades — but the minimum trade count is a **reporting
guideline**, not a hard validation rule, and other methods (e.g. one-sample t-test) may be selected
per experiment. The chosen method/threshold must always be recorded in experiment metadata.
Statistical significance alone is never proof of a robust strategy — must be read together with
out-of-sample performance, walk-forward validation, parameter sensitivity, drawdown, and
risk-adjusted performance.

### Q24 — Train/validation/test split ratios
**Q:** What default split ratios separate training, validation, and out-of-sample test data?
**Decision (accepted as recommended):** 60/20/20, split chronologically (never shuffled) —
preserves the no-lookahead rule.

---

## RISK_ENGINE.md

### Q25 — Default numeric risk limits
**Q:** What are the default limits for max position size, daily loss, drawdown, concurrent
positions?
**Decision (modified):** Max position size 5% of equity (not 10% as recommended, matching Q07's
5% sizing default) — max 2% daily loss, max 20% drawdown (mandatory review warning; a hard stop is
optional per experiment), max 5 concurrent positions — those three unchanged from the
recommendation. All limits configurable per experiment; overrides recorded for reproducibility.

### Q26 — Leverage/margin trading scope
**Q:** Is V1 paper trading spot-only, or does it simulate leveraged perpetual futures?
**Decision (accepted as recommended):** Spot-only for V1. Funding/open-interest data is still
collected for research features now, but leveraged paper trading is a later phase.

### Q27 — Kill-switch trigger thresholds
**Q:** What thresholds should automatically trigger the kill switch?
**Decision (modified):** Same core triggers as recommended (daily loss / drawdown breach, 3+
consecutive execution failures, data feed stale >5 minutes), plus two more: database unavailable,
and a critical data-integrity failure reported by the Data Quality Agent. On trigger: stop opening
new positions, cancel pending paper orders, keep logging/monitoring running, raise a CRITICAL
alert, record the full incident. The kill switch applies to Paper Trading only in V1 and never
terminates Athena itself — data collection and monitoring keep running to support diagnosis.

---

## SYSTEM_ARCHITECTURE.md

### Q28 — Scheduling paradigm for V1
**Q:** What scheduling approach should the centralized scheduler use?
**Decision (accepted as recommended):** In-process (e.g. an asyncio loop), not OS-level cron.

### Q29 — Repository layout — binding or illustrative?
**Q:** Is the documented folder layout mandatory, or adaptable?
**Decision (modified):** Illustrative in naming, but binding in intent — see
[[System Architecture & Repository Layout]]. Each top-level module is a bounded context that
should be independently deployable as a future microservice; directory names may evolve as long as
each module keeps one clear responsibility, module boundaries stay unchanged, and dependencies
follow the documented architecture (e.g. `backend/data/, feature_factory/, research/, risk/,
paper_trading/` is acceptable; a catch-all `misc/`/`utils_everything/` is not).

---

## TESTING.md

### Q30 — Test framework
**Q:** Which Python test framework should be used?
**Decision (accepted as recommended):** pytest — already in use, see
[[Coding Guidelines & Operating Principles]].

### Q31 — Coverage target
**Q:** What minimum coverage percentage counts as "high" for critical modules?
**Decision (modified):** 80% overall (as recommended), but 95% for critical modules — higher than
the recommended 90%. Critical modules: Risk Engine, Portfolio Accounting, Order Execution,
Position Sizing, Performance Metrics. Coverage is a quality indicator, not a goal — tests must
still be deterministic, meaningful, isolated, and behavior-based; artificial coverage inflation via
trivial tests is prohibited.

---

## Cross-document conflicts

### Q32 — Coinbase adapter scope
**Q:** Should `CoinbaseExchange` implement the full `ExchangeAdapter` interface, or just a minimal
price-lookup method?
**Decision (modified):** `CoinbaseExchange` implements the **standard** `ExchangeAdapter`
interface (not a separate lightweight one) but only for a limited scope: symbol discovery, current
price, historical OHLCV, ticker info — used for cross-exchange comparison, data validation, and
market sanity checks. Order execution, paper trading, funding rates, open interest, and private
endpoints are explicitly out of scope for V1 and must raise `NotSupportedError` rather than a
placeholder implementation. Not yet built — and the `Exchange` base contract
([[Exchange Adapter Pattern]]) doesn't yet define a distinct `NotSupportedError` (today's adapters
only use `NotImplementedError` for temporarily-missing methods), so this convention still needs to
be added when Coinbase is implemented.

### Q33 — CryptoPanic/RSS staging
**Q:** Should CryptoPanic/RSS ingestion be built alongside the exchange/macro adapters now, or
deferred?
**Decision (accepted as recommended):** Defer until the core Binance/Bybit/FRED/CoinGecko/
Alternative.me pipeline is solid.

### Q34 — AGENT_PROTOCOL / AI_ARCHITECTURE staging
**Q:** Confirm these describe eventual step-7-equivalent target state only, out of scope until
data/backtesting/risk/paper-trading are complete.
**Decision (accepted as recommended):** Confirmed — target-state specs only, describing
[[Roadmap#Phase 6 — Multi-Agent Research|Phase 6]]. Nothing to build now. See
[[Long-Term Architecture & Development Order#Preferred development order]].

---

## Final decision checklist

- [x] All "decide now" questions answered by the project owner, except Q06 (explicitly deferred)
- [x] V1 scope decisions separated from later/Phase-5+ work
- [ ] Accepted/modified decisions copied into actual implementation docs — still only living in
      `docs/answers_obsidian_optimized.md`; see the warning callout at the top of this note
- [x] Overrides documented with a short reason (see each question's "modified" note above)
- [ ] No unresolved blocker remains before the next round of coding — Q06 still blocks
      [[Roadmap#Phase 3 — Backtesting & Experiment Tracking|Phase 3]]; Q13 (symbol convention) and
      Q32's `NotSupportedError` convention are implemented-decision gaps, not open questions

## Related
- [[Roadmap]]
- [[Trading Research Rules]]
- [[Schemas]]

#athena/decisions
