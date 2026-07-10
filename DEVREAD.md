# DEVREAD.md

## Ambiguity Audit — Project Athena Documentation (`AI Trader.zip`)

This audit reviews the 15 documents in `AI Trader - Kopie/` (AGENT_PROTOCOL, AI_ARCHITECTURE, API_SPECIFICATION, BACKTESTING, CODING_STANDARDS, DATABASE_SCHEMA, DATA_ARCHITECTURE, FEATURE_FACTORY, OBSERVABILITY, PAPER_TRADING, PROJECT_RULES, RESEARCH_PROTOCOL, RISK_ENGINE, SYSTEM_ARCHITECTURE, TESTING) as if implementing Project Athena from scratch. It does not review the architecture or propose new technologies — it identifies every place a real implementer would have to stop and ask the project owner a question before writing correct code.

---

## AGENT_PROTOCOL.md

**1. Request/Response schema — field types undefined**
- Section: "Request Structure" / "Response Structure"
- Blocked because: Fields like `Task ID`, `Timestamp`, `Priority`, `Timeout` are named but never typed (string vs UUID vs int, timestamp format, priority scale/enum, timeout unit/default).
- Ask: What concrete data types, formats, and default values should these fields use?

**2. Confidence semantics undefined**
- Section: "Confidence"
- Blocked because: Doc says confidence "should never be interpreted as statistical certainty" but never defines its scale (0–1 float? Low/Medium/High enum?) or how it's computed.
- Ask: What representation should agent confidence take, and is it self-reported by the LLM or derived from something measurable?

*(Note: whether AGENT_PROTOCOL should be built now at all is a separate, cross-document conflict — see bottom.)*

---

## AI_ARCHITECTURE.md

**3. No LLM provider/model specified anywhere in the doc set**
- Section: "Out of Scope" (explicitly defers this) — but no other document picks it up
- Blocked because: Every "Agent" concept (Research Agent, Data Quality Agent, etc.) requires an actual model/API to call. Given the project's $0-budget constraint, provider choice materially affects feasibility (rate limits, cost caps).
- Ask: Which LLM provider/API (if any) is approved for use, and what is the spend ceiling?

**4. "Version 1 may include" agent list is non-binding**
- Section: "Agent Categories"
- Blocked because: Six agent types are listed with "may include" — not a required set. CLAUDE.md separately names only "Data Quality Agent" as a concrete V1 target.
- Ask: Which of the six listed agents (Research, Documentation, Code Review, Experiment Review, Data Quality, Architecture Assistant) are actually required for V1 vs. aspirational?

---

## API_SPECIFICATION.md

**5. Transport mechanism for V1 unconfirmed**
- Section: "Future Considerations" / "StreamingDataService"
- Blocked because: The doc explicitly says these are "logical interfaces, not HTTP endpoints," and defers REST/gRPC/queues to the future. That implies in-process Python calls for V1, but this is never stated outright, and StreamingDataService's own transport is left fully open ("Future implementations may use... Kafka... NATS" — explicitly forbidden this early per CLAUDE.md).
- Ask: Confirm V1 services are plain in-process Python interfaces, and confirm StreamingDataService can be deferred entirely (no real-time consumers exist yet).

---

## BACKTESTING.md

**6. Default fee and slippage values are unset**
- Section: "Fee Model" / "Default Execution Policy"
- Blocked because: The policy structure is well specified (conservative intrabar fill, exchange-specific fees, fixed slippage) but the actual numbers are never given — "Exchange-specific default values" and "Fixed configurable value" are placeholders, not values.
- Ask: What are the actual default fee percentages (Binance/Bybit maker/taker) and the default fixed slippage value to use out of the box?

**7. Default position sizing model and initial capital**
- Section: "Position Sizing"
- Blocked because: Three sizing models are listed (Fixed Quantity / Fixed Capital / % Equity) with no stated default, and no default starting capital for a backtest run is given anywhere.
- Ask: Which sizing model is the default for a new experiment, and what's the default starting capital?

**8. Overfitting-detection thresholds are qualitative only**
- Section: "Overfitting Detection"
- Blocked because: Warning indicators ("very small trade counts," "unrealistic Sharpe Ratios," "extreme parameter sensitivity") have no numeric thresholds for automatic flagging.
- Ask: What numeric thresholds (e.g., minimum trade count, Sharpe ceiling) should trigger an automatic overfitting warning?

**9. Mandatory benchmark not specified**
- Section: "Benchmark Comparison"
- Blocked because: "Every backtest should compare itself against at least one benchmark" but no default benchmark is designated if the researcher doesn't pick one.
- Ask: Should every experiment auto-run against a fixed default benchmark (e.g., Buy & Hold), or is benchmark selection always manual?

---

## CODING_STANDARDS.md

No blocking ambiguity. Language, formatting tools, naming conventions, import order, exception/logging rules are all concrete and directly implementable as written. (One dependency: it says "every module should include tests" but doesn't name a test framework — tracked under TESTING.md below, not repeated here.)

---

## DATABASE_SCHEMA.md

**10. Numeric precision for price/volume columns**
- Section: "Canonical Market Objects" (referenced) / general schema philosophy
- Blocked because: The schema never specifies decimal precision/scale for prices and volumes. Crypto assets vary wildly (BTC vs. sub-cent tokens), and using the wrong precision silently truncates data — a direct violation of the doc's own "data integrity over performance" principle.
- Ask: What precision/scale (or numeric type) should be used for price and volume columns across all assets?

**11. Canonical timeframe set undefined**
- Section: "candles" table / composite key definition `(exchange_id, symbol_id, timeframe, open_time)`
- Blocked because: "timeframe" is used as a key component throughout, but the doc never enumerates the supported values (1m, 5m, 1h, 1d, etc.) or their storage representation (string vs. interval type).
- Ask: What is the canonical list of supported timeframes for V1, and how should `timeframe` be encoded?

**12. market_sessions default definitions missing**
- Section: "market_sessions"
- Blocked because: Session table purpose is stated ("Asia," "London," "New York") and marked "should remain configurable," but no default time windows (UTC hours) are given.
- Ask: What are the default UTC time boundaries for the Asia/London/New York sessions?

---

## DATA_ARCHITECTURE.md

**13. Canonical symbol/quote-currency convention is inconsistent**
- Section: "Symbol Management"
- Blocked because: The example maps `BTCUSDT → BTC/USD`, silently treating USDT as equivalent to USD. Binance/Bybit trade pairs are actually USDT/USDC/BUSD-denominated, not USD. Whether Athena treats stablecoins as USD-equivalent (and which stablecoin is canonical when multiple exist for the same base asset) is not stated.
- Ask: Should USDT/USDC/BUSD all normalize to a single canonical "USD" quote symbol, or should the stablecoin be preserved as part of the canonical symbol?

**14. Asset and timeframe universe for V1 is unbounded**
- Section: "Supported Data Sources"
- Blocked because: Exchanges are named, but no list of which trading pairs (BTC/USDT only? top-N by volume? a fixed watchlist?) or timeframes to actually ingest is given anywhere in the doc set.
- Ask: What specific symbols and timeframes should the V1 collector target?

**15. Missing-data interpolation trigger mechanism**
- Section: "Missing Data Policy"
- Blocked because: "Interpolation should only occur when explicitly requested" — but by what mechanism (per-query flag? per-dataset config? per-strategy opt-in?) is never specified.
- Ask: How does a consumer "explicitly request" interpolation — is this a config flag, an API parameter, or something else?

**16. Historical backfill depth unspecified**
- Section: "Historical Imports"
- Blocked because: No stated minimum/target history length (e.g., "backfill 5 years of daily candles") for the initial data load.
- Ask: How far back should the initial historical backfill go for each data source?

---

## FEATURE_FACTORY.md

**17. Required V1 feature set and default parameters undefined**
- Section: "Feature Categories"
- Blocked because: Only examples are given per category (EMA, RSI, ATR, etc.) with no required list or default parameter values (e.g., EMA(20) vs EMA(50), RSI(14)?).
- Ask: Which specific features, with which default parameters, must exist in V1's Feature Store?

**18. Feature version numbering scheme undefined**
- Section: "Feature Versioning"
- Blocked because: Versions are referenced as "EMA Version 1 / Version 2" but no actual identifier scheme (integer, semver, hash) is specified.
- Ask: What format should feature version identifiers take?

---

## OBSERVABILITY.md

**19. Logging mechanism and storage target unspecified**
- Section: "Logging" / CODING_STANDARDS' "use the centralized logging framework"
- Blocked because: A "centralized logging framework" is mandated but never defined — where logs are written (file, DB, stdout) and in what format (structured JSON? plain text?) is left open.
- Ask: Where should logs be persisted for V1, and in what format?

**20. Metrics storage/exposure target unspecified**
- Section: "Metrics" / "Data Metrics"
- Blocked because: Metrics like CPU, API latency, and Data Quality Score are listed but it's unclear whether these are meant to land in the `data_quality_reports`/`system_events` tables from DATABASE_SCHEMA.md, or a separate mechanism, since no dashboard exists yet.
- Ask: For V1 (no dashboard), should metrics simply be written to existing System Domain tables, or tracked some other way?

**21. Alert delivery channel unspecified**
- Section: "Alerts"
- Blocked because: Alert conditions are listed (DB unavailable, WebSocket disconnected, etc.) but no delivery mechanism is defined given the $0-budget constraint (no paid alerting service implied).
- Ask: How should alerts reach the project owner in V1 — log-only, local notification, email, something else?

---

## PAPER_TRADING.md

**22. Default starting virtual capital undefined**
- Section: "Virtual Portfolio"
- Blocked because: No default balance is specified for a new paper account.
- Ask: What should the default starting balance be for a new paper trading account?

---

## PROJECT_RULES.md

No blocking ambiguity. This document is a set of cross-cutting priority rules ("data immutable," "AI never controls capital," "live trading forbidden until...") that are all directly enforceable as written; it doesn't introduce new implementation surface.

---

## RESEARCH_PROTOCOL.md

**23. "Statistically significant" has no defined test or threshold**
- Section: "Step 10 — Review"
- Blocked because: The protocol requires judging whether "results were statistically significant" but specifies no test methodology (t-test, bootstrap CI, minimum sample size) or significance level.
- Ask: What statistical method and threshold should Athena use to label a result "statistically significant"?

**24. Train/validation/test split ratios undefined**
- Section: "Out-of-Sample Testing" (referenced from BACKTESTING.md too)
- Blocked because: Data is to be split into Training/Validation/Testing, but no default proportions or date-range convention are given.
- Ask: What default split ratios (or date ranges) should separate training, validation, and out-of-sample test data?

---

## RISK_ENGINE.md

**25. Default numeric risk limits are entirely unset**
- Section: "Maximum Position Size," "Daily Loss Protection," "Drawdown Protection," "Exposure Limits"
- Blocked because: Every limit is described conceptually ("Maximum % of Portfolio," "Maximum Daily Loss") with zero default numbers. A working RiskEngine cannot exist without at least one concrete default configuration.
- Ask: What are the default numeric limits for max position size (%), max daily loss (%), max drawdown (%), and max concurrent positions?

**26. Leverage/margin trading scope unclear**
- Section: "Position Sizing" / "Maximum Leverage"
- Blocked because: The doc set collects funding rates and open interest (implying perpetual futures are tracked) and mentions "Maximum Leverage" as a constraint, but never states whether V1 paper trading actually supports leveraged/margin positions or is spot-only.
- Ask: Is V1 paper trading spot-only, or does it need to simulate leveraged perpetual futures (margin, liquidation, funding payments)?

**27. Kill-switch trigger thresholds unspecified**
- Section: "Kill Switch"
- Blocked because: Triggers are named qualitatively ("extreme drawdown," "repeated execution failures") with no numeric thresholds.
- Ask: What specific thresholds should automatically trigger the kill switch?

---

## SYSTEM_ARCHITECTURE.md

**28. Scheduling paradigm for V1 unspecified**
- Section: "Scheduler"
- Blocked because: A "centralized scheduler" is required for periodic collection/feature generation, but whether V1 should use an in-process async loop, OS-level cron, or something else is left open (message queues are explicitly future-only).
- Ask: What scheduling approach should the centralized scheduler use for V1 (in-process vs. OS-level)?

**29. Repository layout — binding or illustrative?**
- Section: "Project Structure"
- Blocked because: A specific top-level folder tree is given (`athena/backend/data/research/...`) but it's unclear whether this is a mandatory contract or an illustrative example that can be adapted.
- Ask: Is the documented folder layout mandatory, or can it be adapted as long as module responsibilities stay separated?

---

## TESTING.md

**30. Test framework unnamed**
- Section: "Testing Philosophy" / (cross-ref CODING_STANDARDS "Testing")
- Blocked because: Testing is mandatory across the whole platform, but no framework (pytest, unittest, etc.) is named anywhere in the doc set.
- Ask: Which Python test framework should be used?

**31. "High test coverage" has no target percentage**
- Section: "Test Coverage"
- Blocked because: Critical modules (Risk Engine, Portfolio Accounting, etc.) must achieve "high" coverage with no number attached.
- Ask: What minimum coverage percentage counts as "high" for critical modules?

---

## Cross-document conflicts (span multiple files, not fixable by reading one doc alone)

**32. Coinbase adapter scope conflicts between CLAUDE.md and the zip docs**
- Files: CLAUDE.md ("Coinbase: Used as a baseline for price comparison") vs. DATA_ARCHITECTURE.md / SYSTEM_ARCHITECTURE.md (Coinbase listed as a full "Market Data" source alongside Binance/Bybit)
- Blocked because: One source implies a lightweight price-check-only integration; the other implies a full `Exchange` adapter (candles, trades, orderbook, funding).
- Ask: Should `CoinbaseExchange` implement the full `ExchangeAdapter` interface, or only a minimal price-lookup method?

**33. CryptoPanic/RSS staging is ambiguous**
- Files: CLAUDE.md "Version 1 Data Strategy" (lists CryptoPanic & RSS as part of V1) vs. CLAUDE.md "Preferred Development Order" step 1 (lists only "Binance, Bybit, FRED, CoinGecko, Alternative.me" — omits news sources)
- Blocked because: It's unclear whether news ingestion belongs in the very first data-ingestion milestone or a later sub-step within "Version 1."
- Ask: Should CryptoPanic/RSS ingestion be built alongside the exchange/macro adapters now, or deferred to a later V1 sub-phase?

**34. AGENT_PROTOCOL.md / AI_ARCHITECTURE.md describe a fully built multi-agent system, which CLAUDE.md says to refuse building early**
- Files: AGENT_PROTOCOL.md, AI_ARCHITECTURE.md vs. CLAUDE.md ("If asked to build a complex agent system... early, refuse"; AI assistant is step 7 of 8)
- Blocked because: Taken at face value, these two documents read as ready-to-build specs, but CLAUDE.md's staging rule says this work shouldn't start until steps 1–6 are done. Nothing in the docs marks AGENT_PROTOCOL/AI_ARCHITECTURE as "target-state, do not implement yet."
- Ask: Confirm these two documents describe the eventual step-7 target state only, and are explicitly out of scope until data/backtesting/risk/paper-trading are complete.

---

**Sections with no blocking ambiguity:** CODING_STANDARDS.md and PROJECT_RULES.md are fully implementable as written. Most of SYSTEM_ARCHITECTURE.md's layering/dependency rules, DATA_ARCHITECTURE.md's pipeline philosophy, and RESEARCH_PROTOCOL.md's lifecycle steps are also unambiguous — the gaps found are specifically the concrete defaults, numeric thresholds, and scope boundaries needed to actually write code, not the conceptual architecture itself.
