"""Binance REST adapter.

Minimal by design: only `get_candles()`, for later Binance/Bybit price
cross-checks (see AGENTS.md's Data Quality Agent). `get_funding`,
`get_orderbook`, and `get_open_interest` are intentionally left
unimplemented until Bybit's adapter and tests are solid.

Docs: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
"""

from datetime import datetime, timezone

import httpx

from backend.data.adapters.base import Exchange
from backend.data.schemas import CandleRecord, FundingRecord

BASE_URL = "https://api.binance.com"


def _ms_to_utc(ms: int | str) -> datetime:
    return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc)


class BinanceExchange(Exchange):
    def __init__(self, client: httpx.Client | None = None):
        self._client = client or httpx.Client(base_url=BASE_URL, timeout=10.0)

    def get_candles(
        self, symbol: str, timeframe: str, start: datetime, end: datetime
    ) -> list[CandleRecord]:
        response = self._client.get(
            "/api/v3/klines",
            params={
                "symbol": symbol,
                "interval": timeframe,
                "startTime": int(start.timestamp() * 1000),
                "endTime": int(end.timestamp() * 1000),
                "limit": 1000,
            },
        )
        response.raise_for_status()
        rows = response.json()

        now = datetime.now(timezone.utc)
        records = []
        for row in rows:
            (
                open_ms,
                open_,
                high,
                low,
                close,
                volume,
                close_ms,
                *_rest,
            ) = row
            records.append(
                CandleRecord(
                    exchange="binance",
                    symbol=symbol,
                    timeframe=timeframe,
                    open_time=_ms_to_utc(open_ms),
                    close_time=_ms_to_utc(close_ms),
                    open=float(open_),
                    high=float(high),
                    low=float(low),
                    close=float(close),
                    volume=float(volume),
                    ingestion_time=now,
                    raw_payload={"row": row},
                )
            )
        return records

    def get_funding(self, symbol: str, start: datetime, end: datetime) -> list[FundingRecord]:
        raise NotImplementedError("BinanceExchange.get_funding is not implemented in V1")

    def get_orderbook(self, symbol: str):
        raise NotImplementedError("BinanceExchange.get_orderbook is not implemented in V1")

    def get_open_interest(self, symbol: str, start: datetime, end: datetime):
        raise NotImplementedError(
            "BinanceExchange.get_open_interest is not implemented in V1"
        )
