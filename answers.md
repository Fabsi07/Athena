# answers.md

Working copy of the 34 open questions from `DEVREAD.md`. Each item has a **Claude recommends** line (with brief why) and a blank **Your answer:** line for you to fill in, override, or leave as-is after sleeping on it. Full reasoning for why each question blocks implementation is in `DEVREAD.md`.

---

## AGENT_PROTOCOL.md

**1. Request/Response schema — field types**
Q: What concrete data types, formats, and default values should Task ID, Timestamp, Priority, Timeout use?
Claude recommends: Task ID = UUID4 string; Timestamp = ISO-8601 UTC; Priority = enum `{LOW, NORMAL, HIGH}` default NORMAL; Timeout = int seconds, default 120s, overridable per task type. Simple and typed, nothing fancy needed.
Your answer:

**2. Confidence semantics**
Q: What representation should agent confidence take, and is it self-reported or derived?
Claude recommends: Plain float 0.0–1.0, self-reported by the agent. There's no ground truth for research judgments to derive it from, and per CLAUDE.md it must never feed position sizing anyway.
Your answer:

---

## AI_ARCHITECTURE.md

**3. LLM provider/model**
Q: Which LLM provider/API (if any) is approved for use, and what is the spend ceiling?
Claude recommends: Don't decide this now — it's step 7 work. When it comes up, default to whatever Claude access you already have via your existing subscription (with a hard spend cap) rather than integrating a new vendor.
Your answer:

**4. V1 agent set**
Q: Which of the six listed agents are actually required for V1 vs. aspirational?
Claude recommends: Only the Data Quality Agent — it's the one CLAUDE.md names explicitly as a "good AI use" today. Everything else (Research, Documentation, Code Review, Experiment Review, Architecture Assistant) waits for step 7.
Your answer:

---

## API_SPECIFICATION.md

**5. Transport mechanism for V1**
Q: Confirm V1 services are plain in-process Python interfaces, and confirm StreamingDataService can be deferred.
Claude recommends: Yes to both — in-process Python calls only, no HTTP/gRPC/queues. Defer StreamingDataService entirely until Paper Trading (step 6) actually needs a live feed.
Your answer:

---

## BACKTESTING.md

**6. Default fee and slippage values**
Q: What are the actual default fee percentages and default fixed slippage value?
Claude recommends: ~0.1% taker/maker spot on Binance/Bybit, ~0.05–0.06% taker on perps; flat 5 bps slippage per trade. Always use the taker fee even for "market orders" — conservative per CLAUDE.md's fill-assumption rule.
Your answer:

**7. Default position sizing model and initial capital**
Q: Which sizing model is the default, and what's the default starting capital?
Claude recommends: "% of Equity" sizing (100% notional per signal, single-asset backtest) with $10,000 starting capital — round number, easy to sanity-check % returns.
Your answer:

**8. Overfitting-detection thresholds**
Q: What numeric thresholds should trigger an automatic overfitting warning?
Claude recommends: Flag if trade count < 30, annualized Sharpe > 3, or a ±10–20% parameter change swings performance by >50%. Standard quant-research rules of thumb.
Your answer:

**9. Mandatory benchmark**
Q: Should every experiment auto-run against a fixed default benchmark, or is it always manual?
Claude recommends: Auto-run Buy & Hold (same asset/timeframe) for every experiment by default; anything else is opt-in.
Your answer:

---

## CODING_STANDARDS.md

No open questions — fully implementable as written.

---

## DATABASE_SCHEMA.md

**10. Numeric precision for price/volume columns**
Q: What precision/scale should be used for price and volume columns?
Claude recommends: `NUMERIC(20,8)` — standard crypto precision, handles both satoshi-level pricing and large volume figures.
Your answer:

**11. Canonical timeframe set**
Q: What is the canonical list of supported timeframes, and how should `timeframe` be encoded?
Claude recommends: Start minimal — `1h`, `1d` only, stored as a short string enum. Add `1m`/`5m` later only if a strategy actually needs them, to keep storage/compute small on a $0 budget.
Your answer:

**12. market_sessions default definitions**
Q: What are the default UTC time boundaries for the Asia/London/New York sessions?
Claude recommends: Asia 00:00–09:00 UTC, London 08:00–16:00 UTC, New York 13:00–21:00 UTC (standard forex session convention).
Your answer:

---

## DATA_ARCHITECTURE.md

**13. Canonical symbol/quote-currency convention**
Q: Should USDT/USDC/BUSD normalize to "USD", or should the stablecoin be preserved?
Claude recommends: Preserve it — canonical symbol should be `BTC/USDT`, not `BTC/USD`. Stablecoins de-peg sometimes; collapsing them destroys real information and cuts against the data-integrity principle. (This is the one place I'd push back on the doc's own example.)
Your answer:

**14. Asset and timeframe universe for V1**
Q: What specific symbols and timeframes should the V1 collector target?
Claude recommends: Start narrow — BTC, ETH (maybe SOL) vs USDT, on Binance + Bybit. Expand once the pipeline is proven reliable.
Your answer:

**15. Missing-data interpolation trigger mechanism**
Q: How does a consumer "explicitly request" interpolation?
Claude recommends: A simple boolean query parameter (`allow_interpolation=False` by default) rather than a config file or global flag — keeps it obvious at the call site.
Your answer:

**16. Historical backfill depth**
Q: How far back should the initial historical backfill go?
Claude recommends: Pull the maximum history the free APIs allow (Binance/Bybit klines go back to listing date). Storage is cheap; more history is strictly better for research.
Your answer:

---

## FEATURE_FACTORY.md

**17. Required V1 feature set and default parameters**
Q: Which specific features, with which default parameters, must exist in V1?
Claude recommends: Keep it small at first — EMA(20/50/200), RSI(14), ATR(14), rolling realized volatility. Enough to support a first simple strategy; grow from there.
Your answer:

**18. Feature version numbering scheme**
Q: What format should feature version identifiers take?
Claude recommends: Plain incrementing integer (`EMA_v1`, `EMA_v2`) — matches the doc's own examples, no need for semver complexity.
Your answer:

---

## OBSERVABILITY.md

**19. Logging mechanism and storage target**
Q: Where should logs be persisted, and in what format?
Claude recommends: Python's standard `logging` module, structured JSON lines, written to local rotating log files — logs are operational, not business data, so they don't belong in the DB.
Your answer:

**20. Metrics storage/exposure target**
Q: Should metrics be written to existing System Domain tables, or tracked some other way?
Claude recommends: Write into the `system_events` / `data_quality_reports` tables already defined in DATABASE_SCHEMA.md. No separate metrics stack — avoids new infra on a $0 budget.
Your answer:

**21. Alert delivery channel**
Q: How should alerts reach the project owner in V1?
Claude recommends: ERROR/CRITICAL log entries plus, optionally, a simple SMTP email to yourself. No paid alerting service needed yet.
Your answer:

---

## PAPER_TRADING.md

**22. Default starting virtual capital**
Q: What should the default starting balance be for a new paper trading account?
Claude recommends: $10,000, matching the backtest default so results are directly comparable.
Your answer:

---

## PROJECT_RULES.md

No open questions — fully implementable as written.

---

## RESEARCH_PROTOCOL.md

**23. "Statistically significant" test/threshold**
Q: What statistical method and threshold should Athena use?
Claude recommends: Bootstrap resampling on trade returns (or a one-sample t-test that mean return > 0), p < 0.05, and a minimum of 30 trades before any significance claim is made at all.
Your answer:

**24. Train/validation/test split ratios**
Q: What default split ratios should separate training, validation, and out-of-sample test data?
Claude recommends: 60/20/20, split chronologically (never shuffled) — preserves the no-lookahead rule.
Your answer:

---

## RISK_ENGINE.md

**25. Default numeric risk limits**
Q: What are the default limits for max position size, daily loss, drawdown, concurrent positions?
Claude recommends: Max 10% of equity per position; max 2% daily loss; max 20% drawdown (triggers a review, not necessarily a hard stop); max 5 concurrent positions. Conservative retail-quant defaults, all overridable per experiment.
Your answer:

**26. Leverage/margin trading scope**
Q: Is V1 paper trading spot-only, or does it simulate leveraged perpetual futures?
Claude recommends: Spot-only for V1. Funding rate/open interest data gets collected for research features now, but actual leveraged/margin paper trading is a later phase — much simpler risk engine, consistent with "no live trades until mature."
Your answer:

**27. Kill-switch trigger thresholds**
Q: What specific thresholds should automatically trigger the kill switch?
Claude recommends: Daily loss limit breached, OR max drawdown breached, OR 3+ consecutive execution failures, OR market data feed stale for >5 minutes.
Your answer:

---

## SYSTEM_ARCHITECTURE.md

**28. Scheduling paradigm for V1**
Q: What scheduling approach should the centralized scheduler use?
Claude recommends: In-process (e.g. an asyncio-based loop inside the app), not OS-level cron. Simpler for a single local machine and portable across dev machines.
Your answer:

**29. Repository layout — binding or illustrative?**
Q: Is the documented folder layout mandatory, or can it be adapted?
Claude recommends: Treat as illustrative. Your current repo (`backend/data/adapters`, etc.) already diverges slightly from the doc's example tree — that's fine as long as each module keeps one clear responsibility.
Your answer:

---

## TESTING.md

**30. Test framework**
Q: Which Python test framework should be used?
Claude recommends: pytest — the de facto Python standard, plays well with your existing `pyproject.toml`.
Your answer:

**31. Coverage target**
Q: What minimum coverage percentage counts as "high" for critical modules?
Claude recommends: 80% overall, 90%+ for Risk Engine and Portfolio Accounting specifically.
Your answer:

---

## Cross-document conflicts

**32. Coinbase adapter scope**
Q: Should `CoinbaseExchange` implement the full `ExchangeAdapter` interface, or only a minimal price-lookup method?
Claude recommends: Lightweight adapter — just price/ticker lookup for cross-exchange divergence checks. Don't build out orderbook/funding for it; matches CLAUDE.md's "baseline for price comparison" framing, and Coinbase spot doesn't have funding rates anyway.
Your answer:

**33. CryptoPanic/RSS staging**
Q: Should CryptoPanic/RSS ingestion be built alongside the exchange/macro adapters now, or deferred?
Claude recommends: Defer until the core Binance/Bybit/FRED/CoinGecko/Alternative.me pipeline is solid — matches the literal step-1 list in CLAUDE.md, which omits news sources.
Your answer:

**34. AGENT_PROTOCOL / AI_ARCHITECTURE staging**
Q: Confirm these two documents describe the eventual step-7 target state only, and are out of scope until data/backtesting/risk/paper-trading are complete.
Claude recommends: Confirmed yes — these are step-7 target-state specs only. Nothing to build now.
Your answer:
