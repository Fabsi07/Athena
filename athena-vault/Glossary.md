---
title: Glossary
tags: [athena, reference]
---

# Glossary

**Exchange adapter** — a concrete subclass of the `Exchange` abstract base class
([[Exchange Adapter Pattern]]) that translates one exchange's API into Athena's typed record
format. The only place external market-data API calls are allowed.

**Hypertable** — a TimescaleDB table automatically partitioned by time. Both `candles` and
`funding_rates` are hypertables — see [[TimescaleDB Storage]].

**Idempotent ingestion** — re-running the same fetch never duplicates rows, enforced via
composite primary keys and `ON CONFLICT DO NOTHING` — see [[TimescaleDB Storage]].

**Lookahead bias** — using information in a backtest that would not actually have been knowable
at that point in time. See [[Trading Research Rules]].

**Out-of-sample** — data or a result derived from data that was not used to design or tune the
strategy being evaluated. See [[Trading Research Rules]].

**Raw payload** — the unmodified JSON response from an exchange API, preserved alongside parsed
fields on every record (`raw_payload` in [[Schemas]]), so nothing is lost to premature
transformation.

**Result stage** — one of five explicit labels (hypothesis, backtest, out-of-sample, paper trade,
live trade) that every research result must carry. See [[Trading Research Rules]].

**Settlement time vs. raw timestamp** — two deliberately separate datetime fields on
`FundingRecord` ([[Schemas]]): the exchange's raw reported timestamp vs. Athena's own interpreted
settlement instant, kept apart to avoid baking in lookahead assumptions.

**Survivorship bias** — evaluating a strategy only on assets/data that "survived" to the present,
skewing results optimistically. See [[Trading Research Rules]].

**V1 / Version 1** — the current build phase: $0 budget, free-tier data only, local TimescaleDB,
no message brokers, no live trading. See [[North Star]].

## Related
- [[Home]]
- [[Trading Research Rules]]
- [[Schemas]]

#athena/reference
