-- Project Athena V1 storage schema.
-- Tables hold pre-validated records only; no transformation happens here.

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS candles (
    exchange        TEXT NOT NULL,
    symbol          TEXT NOT NULL,
    timeframe       TEXT NOT NULL,
    open_time       TIMESTAMPTZ NOT NULL,
    close_time      TIMESTAMPTZ NOT NULL,
    open            DOUBLE PRECISION NOT NULL,
    high            DOUBLE PRECISION NOT NULL,
    low             DOUBLE PRECISION NOT NULL,
    close           DOUBLE PRECISION NOT NULL,
    volume          DOUBLE PRECISION NOT NULL,
    ingestion_time  TIMESTAMPTZ NOT NULL,
    raw_payload     JSONB,
    PRIMARY KEY (exchange, symbol, timeframe, open_time)
);

SELECT create_hypertable('candles', 'open_time', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS funding_rates (
    exchange                 TEXT NOT NULL,
    symbol                   TEXT NOT NULL,
    funding_timestamp_raw    TIMESTAMPTZ NOT NULL,
    funding_settlement_time  TIMESTAMPTZ NOT NULL,
    funding_rate             DOUBLE PRECISION NOT NULL,
    ingestion_time           TIMESTAMPTZ NOT NULL,
    raw_payload               JSONB,
    PRIMARY KEY (exchange, symbol, funding_timestamp_raw)
);

SELECT create_hypertable(
    'funding_rates', 'funding_timestamp_raw', if_not_exists => TRUE
);
