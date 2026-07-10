---
title: TimescaleDB Storage
tags: [athena, data, storage]
source: backend/data/storage/schema.sql, backend/data/storage/timescale_writer.py, docker-compose.yml
---

# TimescaleDB Storage

TimescaleDB, run locally via Docker Compose, **pinned to a specific image tag** (never `latest`,
for reproducibility): `timescale/timescaledb:2.15.0-pg16`.

## Schema (`backend/data/storage/schema.sql`)

> [!quote]
> Tables hold pre-validated records only; no transformation happens here.

```sql
CREATE TABLE candles (
    exchange, symbol, timeframe, open_time, close_time,
    open, high, low, close, volume,
    ingestion_time, raw_payload JSONB,
    PRIMARY KEY (exchange, symbol, timeframe, open_time)
);
SELECT create_hypertable('candles', 'open_time', if_not_exists => TRUE);

CREATE TABLE funding_rates (
    exchange, symbol, funding_timestamp_raw, funding_settlement_time,
    funding_rate, ingestion_time, raw_payload JSONB,
    PRIMARY KEY (exchange, symbol, funding_timestamp_raw)
);
SELECT create_hypertable('funding_rates', 'funding_timestamp_raw', if_not_exists => TRUE);
```

Both tables are TimescaleDB **hypertables**, partitioned by their time column, matching the
fields defined in [[Schemas]].

## Idempotency

The composite primary keys make repeated ingestion safe: re-running the same fetch inserts
`ON CONFLICT DO NOTHING` instead of erroring or duplicating rows. This matters because ingestion
scripts are expected to be re-run (e.g. after a crash, or to backfill overlapping ranges) without
manual deduplication.

## Writer (`backend/data/storage/timescale_writer.py`)

`TimescaleWriter` is intentionally dumb:

- `write_candles(records: list[CandleRecord]) -> int` and
  `write_funding(records: list[FundingRecord]) -> int` — both use
  `psycopg2.extras.execute_values` with `ON CONFLICT DO NOTHING RETURNING 1`, returning the count
  of rows *actually* written (i.e. excluding conflicts).
- **Zero transformation logic.** It only accepts records that already passed
  `backend.data.schemas` validation — the writer trusts the type system, not the other way around.
- Connection parameters come from environment variables (`POSTGRES_HOST`, `POSTGRES_PORT`,
  `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`), defaulting to `localhost` / `athena` /
  `changeme` / `athena` — matching `docker-compose.yml`'s defaults.

## Local setup

```yaml
services:
  timescaledb:
    image: timescale/timescaledb:2.15.0-pg16
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-athena}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
      POSTGRES_DB: ${POSTGRES_DB:-athena}
    ports: ["${POSTGRES_PORT:-5432}:5432"]
    volumes:
      - timescale_data:/var/lib/postgresql/data
      - ./backend/data/storage/schema.sql:/docker-entrypoint-initdb.d/schema.sql:ro
```

The schema file is mounted directly into Postgres's init directory, so `docker compose up -d` on a
fresh volume creates the tables automatically — see [[Getting Started]].

## Related
- [[Schemas]]
- [[Exchange Adapters]]
- [[Open Questions Log#Q10 — Numeric precision for price/volume columns|Q10]] — open question on whether `DOUBLE PRECISION` should become `NUMERIC(20,8)`

#athena/data
