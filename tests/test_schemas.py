from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from backend.data.schemas import CandleRecord, FundingRecord

UTC_NOW = datetime(2024, 1, 1, tzinfo=timezone.utc)
NAIVE_NOW = datetime(2024, 1, 1)
NON_UTC_NOW = datetime(2024, 1, 1, tzinfo=timezone(timedelta(hours=2)))


def _candle_kwargs(**overrides):
    kwargs = dict(
        exchange="bybit",
        symbol="BTCUSDT",
        timeframe="1h",
        open_time=UTC_NOW,
        close_time=UTC_NOW,
        open=100.0,
        high=101.0,
        low=99.0,
        close=100.5,
        volume=10.0,
        ingestion_time=UTC_NOW,
    )
    kwargs.update(overrides)
    return kwargs


def _funding_kwargs(**overrides):
    kwargs = dict(
        exchange="bybit",
        symbol="BTCUSDT",
        funding_timestamp_raw=UTC_NOW,
        funding_settlement_time=UTC_NOW,
        funding_rate=0.0001,
        ingestion_time=UTC_NOW,
    )
    kwargs.update(overrides)
    return kwargs


def test_candle_record_accepts_utc_datetimes():
    record = CandleRecord(**_candle_kwargs())
    assert record.open_time == UTC_NOW


def test_candle_record_rejects_naive_datetime():
    with pytest.raises(ValidationError):
        CandleRecord(**_candle_kwargs(open_time=NAIVE_NOW))


def test_candle_record_rejects_non_utc_datetime():
    with pytest.raises(ValidationError):
        CandleRecord(**_candle_kwargs(open_time=NON_UTC_NOW))


@pytest.mark.parametrize("field", ["open", "high", "low", "close", "volume"])
def test_candle_record_rejects_negative_values(field):
    with pytest.raises(ValidationError):
        CandleRecord(**_candle_kwargs(**{field: -1.0}))


def test_candle_record_raw_payload_round_trips():
    payload = {"raw": "data", "nested": {"a": 1}}
    record = CandleRecord(**_candle_kwargs(raw_payload=payload))
    assert record.raw_payload == payload
    assert record.model_validate(record.model_dump()).raw_payload == payload


def test_funding_record_accepts_utc_datetimes():
    record = FundingRecord(**_funding_kwargs())
    assert record.funding_timestamp_raw == UTC_NOW
    assert record.funding_settlement_time == UTC_NOW


def test_funding_record_rejects_naive_datetime():
    with pytest.raises(ValidationError):
        FundingRecord(**_funding_kwargs(funding_timestamp_raw=NAIVE_NOW))


def test_funding_record_raw_payload_round_trips():
    payload = {"retCode": 0, "result": {"list": []}}
    record = FundingRecord(**_funding_kwargs(raw_payload=payload))
    assert record.raw_payload == payload
    assert record.model_validate(record.model_dump()).raw_payload == payload
