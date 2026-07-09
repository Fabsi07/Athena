from datetime import datetime, timezone

import psycopg2
import pytest

from backend.data.schemas import FundingRecord
from backend.data.storage.timescale_writer import TimescaleWriter, _connection_params


def _get_connection():
    try:
        return psycopg2.connect(**_connection_params())
    except psycopg2.OperationalError:
        return None


@pytest.fixture
def conn():
    connection = _get_connection()
    if connection is None:
        pytest.skip(
            "TimescaleDB not reachable — start it with `docker compose up -d` "
            "and re-run this test"
        )
    yield connection
    connection.close()


def _funding_record(**overrides):
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)
    kwargs = dict(
        exchange="bybit",
        symbol="BTCUSDT",
        funding_timestamp_raw=now,
        funding_settlement_time=now,
        funding_rate=0.0001,
        ingestion_time=now,
        raw_payload={"test": True},
    )
    kwargs.update(overrides)
    return FundingRecord(**kwargs)


def test_write_funding_is_idempotent(conn):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM funding_rates WHERE exchange = 'bybit_test'")
    conn.commit()

    record = _funding_record(exchange="bybit_test")
    writer = TimescaleWriter(conn=conn)

    first_written = writer.write_funding([record])
    second_written = writer.write_funding([record])

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM funding_rates WHERE exchange = 'bybit_test'"
        )
        (row_count,) = cursor.fetchone()

    assert first_written == 1
    assert second_written == 0
    assert row_count == 1

    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM funding_rates WHERE exchange = 'bybit_test'")
    conn.commit()
