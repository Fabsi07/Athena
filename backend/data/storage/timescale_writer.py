"""Writes pre-validated records to TimescaleDB.

This module contains zero transformation logic. It only accepts records
that have already passed through `backend.data.schemas` validation and
inserts them idempotently via `ON CONFLICT DO NOTHING`.
"""

import os

import psycopg2
import psycopg2.extras

from backend.data.schemas import CandleRecord, FundingRecord


def _connection_params() -> dict:
    return {
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": int(os.environ.get("POSTGRES_PORT", "5432")),
        "user": os.environ.get("POSTGRES_USER", "athena"),
        "password": os.environ.get("POSTGRES_PASSWORD", "changeme"),
        "dbname": os.environ.get("POSTGRES_DB", "athena"),
    }


class TimescaleWriter:
    def __init__(self, conn=None):
        self._conn = conn or psycopg2.connect(**_connection_params())

    def close(self) -> None:
        self._conn.close()

    def write_candles(self, records: list[CandleRecord]) -> int:
        if not records:
            return 0
        rows = [
            (
                r.exchange,
                r.symbol,
                r.timeframe,
                r.open_time,
                r.close_time,
                r.open,
                r.high,
                r.low,
                r.close,
                r.volume,
                r.ingestion_time,
                psycopg2.extras.Json(r.raw_payload),
            )
            for r in records
        ]
        with self._conn.cursor() as cursor:
            written = psycopg2.extras.execute_values(
                cursor,
                """
                INSERT INTO candles (
                    exchange, symbol, timeframe, open_time, close_time,
                    open, high, low, close, volume, ingestion_time, raw_payload
                ) VALUES %s
                ON CONFLICT (exchange, symbol, timeframe, open_time) DO NOTHING
                RETURNING 1
                """,
                rows,
                fetch=True,
            )
        self._conn.commit()
        return len(written)

    def write_funding(self, records: list[FundingRecord]) -> int:
        if not records:
            return 0
        rows = [
            (
                r.exchange,
                r.symbol,
                r.funding_timestamp_raw,
                r.funding_settlement_time,
                r.funding_rate,
                r.ingestion_time,
                psycopg2.extras.Json(r.raw_payload),
            )
            for r in records
        ]
        with self._conn.cursor() as cursor:
            written = psycopg2.extras.execute_values(
                cursor,
                """
                INSERT INTO funding_rates (
                    exchange, symbol, funding_timestamp_raw,
                    funding_settlement_time, funding_rate, ingestion_time,
                    raw_payload
                ) VALUES %s
                ON CONFLICT (exchange, symbol, funding_timestamp_raw) DO NOTHING
                RETURNING 1
                """,
                rows,
                fetch=True,
            )
        self._conn.commit()
        return len(written)
