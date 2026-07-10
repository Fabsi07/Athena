"""Typed contracts for market data records.

Every record stored to TimescaleDB must pass through one of these models
first. No transformation logic lives downstream of validation here.
"""

from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, field_validator


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware (naive datetimes are rejected)")
    if value.utcoffset() != timezone.utc.utcoffset(value):
        raise ValueError("datetime must be normalized to UTC")
    return value


class CandleRecord(BaseModel):
    exchange: str
    symbol: str
    timeframe: str
    open_time: datetime
    close_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    ingestion_time: datetime
    raw_payload: dict | None = None

    @field_validator("open_time", "close_time", "ingestion_time")
    @classmethod
    def _validate_utc(cls, value: datetime) -> datetime:
        return _require_utc(value)

    @field_validator("open", "high", "low", "close", "volume")
    @classmethod
    def _validate_non_negative(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("price and volume fields must be non-negative")
        return value


class FundingRecord(BaseModel):
    """A single funding-rate observation.

    `funding_timestamp_raw` is the timestamp exactly as reported by the
    exchange. `funding_settlement_time` is our own interpreted UTC datetime
    for when the rate actually settled. These are kept as separate fields
    on purpose: when this information was actually knowable/tradable must
    be modeled separately later, to avoid lookahead bias.
    """

    exchange: str
    symbol: str
    funding_timestamp_raw: datetime
    funding_settlement_time: datetime
    funding_rate: Decimal
    ingestion_time: datetime
    raw_payload: dict | None = None

    @field_validator(
        "funding_timestamp_raw", "funding_settlement_time", "ingestion_time"
    )
    @classmethod
    def _validate_utc(cls, value: datetime) -> datetime:
        return _require_utc(value)
