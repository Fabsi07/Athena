from datetime import datetime, timezone
from decimal import Decimal

import httpx
import pytest
import respx

from backend.data.adapters.bybit import BASE_URL, BybitExchange

START = datetime(2024, 1, 1, tzinfo=timezone.utc)
END = datetime(2024, 1, 2, tzinfo=timezone.utc)


def _exchange():
    return BybitExchange(client=httpx.Client(base_url=BASE_URL, timeout=10.0))


@respx.mock
def test_get_funding_parses_and_normalizes_utc():
    respx.get(f"{BASE_URL}/v5/market/funding/history").mock(
        return_value=httpx.Response(
            200,
            json={
                "retCode": 0,
                "retMsg": "OK",
                "result": {
                    "category": "linear",
                    "list": [
                        {
                            "symbol": "BTCUSDT",
                            "fundingRate": "0.0001",
                            "fundingRateTimestamp": "1704067200000",
                        }
                    ],
                },
                "retExtInfo": {},
                "time": 1704067200000,
            },
        )
    )

    records = _exchange().get_funding("BTCUSDT", START, END)

    assert len(records) == 1
    record = records[0]
    assert record.exchange == "bybit"
    assert record.symbol == "BTCUSDT"
    assert record.funding_rate == Decimal("0.0001")
    assert record.funding_timestamp_raw == datetime(2024, 1, 1, tzinfo=timezone.utc)
    assert record.funding_settlement_time == datetime(2024, 1, 1, tzinfo=timezone.utc)
    assert record.raw_payload == {
        "symbol": "BTCUSDT",
        "fundingRate": "0.0001",
        "fundingRateTimestamp": "1704067200000",
    }


def test_funding_record_has_separate_raw_and_settlement_fields():
    from backend.data.schemas import FundingRecord

    assert "funding_timestamp_raw" in FundingRecord.model_fields
    assert "funding_settlement_time" in FundingRecord.model_fields


@respx.mock
def test_get_candles_parses_and_computes_close_time():
    respx.get(f"{BASE_URL}/v5/market/kline").mock(
        return_value=httpx.Response(
            200,
            json={
                "retCode": 0,
                "retMsg": "OK",
                "result": {
                    "symbol": "BTCUSDT",
                    "category": "linear",
                    "list": [
                        [
                            "1704067200000",
                            "100.0",
                            "101.0",
                            "99.0",
                            "100.5",
                            "10.0",
                            "1000.0",
                        ]
                    ],
                },
                "retExtInfo": {},
                "time": 1704067200000,
            },
        )
    )

    records = _exchange().get_candles("BTCUSDT", "1h", START, END)

    assert len(records) == 1
    record = records[0]
    assert record.timeframe == "1h"
    assert record.open_time == datetime(2024, 1, 1, tzinfo=timezone.utc)
    assert record.close_time == datetime(
        2024, 1, 1, 0, 59, 59, 999000, tzinfo=timezone.utc
    )
    assert record.open == Decimal("100.0")
    assert record.volume == Decimal("10.0")


@respx.mock
def test_get_funding_raises_on_non_2xx_http():
    respx.get(f"{BASE_URL}/v5/market/funding/history").mock(
        return_value=httpx.Response(500, json={"error": "server error"})
    )

    with pytest.raises(httpx.HTTPStatusError):
        _exchange().get_funding("BTCUSDT", START, END)


@respx.mock
def test_get_funding_raises_on_ret_code_error():
    respx.get(f"{BASE_URL}/v5/market/funding/history").mock(
        return_value=httpx.Response(
            200,
            json={
                "retCode": 10001,
                "retMsg": "params error",
                "result": {},
                "retExtInfo": {},
                "time": 1704067200000,
            },
        )
    )

    with pytest.raises(RuntimeError, match="retCode=10001"):
        _exchange().get_funding("BTCUSDT", START, END)


def test_get_candles_rejects_unsupported_interval():
    with pytest.raises(ValueError, match="unsupported"):
        _exchange().get_candles("BTCUSDT", "not-a-real-interval", START, END)
