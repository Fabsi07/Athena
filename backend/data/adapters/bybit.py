"""Bybit V5 REST adapter.

Docs: https://bybit-exchange.github.io/docs/v5/market/funding-rate
      https://bybit-exchange.github.io/docs/v5/market/kline

Bybit returns HTTP 200 even on API-level errors, with the real status in
the `retCode` field of the JSON body. Both HTTP-level and retCode-level
failures must raise -- neither is optional.
"""

from datetime import datetime, timezone

import httpx

from backend.data.adapters.base import Exchange
from backend.data.schemas import CandleRecord, FundingRecord

BASE_URL = "https://api.bybit.com"

# Bybit kline interval -> duration in milliseconds. Only intervals we've
# verified the math for are listed; unsupported intervals raise rather
# than guess at a candle's close time.
_INTERVAL_MS = {
    "1": 60_000,
    "3": 3 * 60_000,
    "5": 5 * 60_000,
    "15": 15 * 60_000,
    "30": 30 * 60_000,
    "60": 60 * 60_000,
    "120": 2 * 60 * 60_000,
    "240": 4 * 60 * 60_000,
    "360": 6 * 60 * 60_000,
    "720": 12 * 60 * 60_000,
    "D": 24 * 60 * 60_000,
    "W": 7 * 24 * 60 * 60_000,
}


def _ms_to_utc(ms: int | str) -> datetime:
    return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc)


class BybitExchange(Exchange):
    def __init__(self, client: httpx.Client | None = None, category: str = "linear"):
        self._client = client or httpx.Client(base_url=BASE_URL, timeout=10.0)
        self._category = category

    def _get(self, path: str, params: dict) -> dict:
        response = self._client.get(path, params=params)
        response.raise_for_status()
        body = response.json()
        if body.get("retCode") != 0:
            raise RuntimeError(
                f"Bybit API error retCode={body.get('retCode')} "
                f"retMsg={body.get('retMsg')!r} for {path}"
            )
        return body

    def get_funding(
        self, symbol: str, start: datetime, end: datetime
    ) -> list[FundingRecord]:
        body = self._get(
            "/v5/market/funding/history",
            params={
                "category": self._category,
                "symbol": symbol,
                "startTime": int(start.timestamp() * 1000),
                "endTime": int(end.timestamp() * 1000),
                "limit": 200,
            },
        )
        now = datetime.now(timezone.utc)
        records = []
        for entry in body["result"]["list"]:
            # Bybit's `fundingRateTimestamp` is documented as the settlement
            # instant itself (not an interval start we'd need to interpret),
            # so raw and settlement carry the same value here. They stay
            # separate fields because that won't hold for every exchange.
            timestamp = _ms_to_utc(entry["fundingRateTimestamp"])
            records.append(
                FundingRecord(
                    exchange="bybit",
                    symbol=entry["symbol"],
                    funding_timestamp_raw=timestamp,
                    funding_settlement_time=timestamp,
                    funding_rate=float(entry["fundingRate"]),
                    ingestion_time=now,
                    raw_payload=entry,
                )
            )
        return records

    def get_candles(
        self, symbol: str, timeframe: str, start: datetime, end: datetime
    ) -> list[CandleRecord]:
        if timeframe not in _INTERVAL_MS:
            raise ValueError(f"unsupported Bybit kline interval: {timeframe!r}")
        interval_ms = _INTERVAL_MS[timeframe]

        body = self._get(
            "/v5/market/kline",
            params={
                "category": self._category,
                "symbol": symbol,
                "interval": timeframe,
                "start": int(start.timestamp() * 1000),
                "end": int(end.timestamp() * 1000),
                "limit": 1000,
            },
        )
        now = datetime.now(timezone.utc)
        records = []
        for open_ms, open_, high, low, close, volume, turnover in body["result"]["list"]:
            open_time = _ms_to_utc(open_ms)
            close_time = _ms_to_utc(int(open_ms) + interval_ms - 1)
            records.append(
                CandleRecord(
                    exchange="bybit",
                    symbol=body["result"]["symbol"],
                    timeframe=timeframe,
                    open_time=open_time,
                    close_time=close_time,
                    open=float(open_),
                    high=float(high),
                    low=float(low),
                    close=float(close),
                    volume=float(volume),
                    ingestion_time=now,
                    raw_payload={
                        "start": open_ms,
                        "open": open_,
                        "high": high,
                        "low": low,
                        "close": close,
                        "volume": volume,
                        "turnover": turnover,
                    },
                )
            )
        return records

    def get_orderbook(self, symbol: str):
        raise NotImplementedError("BybitExchange.get_orderbook is not implemented in V1")

    def get_open_interest(self, symbol: str, start: datetime, end: datetime):
        raise NotImplementedError(
            "BybitExchange.get_open_interest is not implemented in V1"
        )
