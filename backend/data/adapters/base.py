"""The Exchange abstraction mandated by AGENTS.md's Adapter Mandate.

No file outside `backend/data/adapters/` may call an exchange API directly.
Research, backtesting, and strategy code must go through a concrete
subclass of `Exchange`.
"""

from abc import ABC, abstractmethod
from datetime import datetime

from backend.data.schemas import CandleRecord, FundingRecord


class Exchange(ABC):
    @abstractmethod
    def get_candles(
        self, symbol: str, timeframe: str, start: datetime, end: datetime
    ) -> list[CandleRecord]:
        raise NotImplementedError

    @abstractmethod
    def get_funding(
        self, symbol: str, start: datetime, end: datetime
    ) -> list[FundingRecord]:
        raise NotImplementedError

    @abstractmethod
    def get_orderbook(self, symbol: str):
        raise NotImplementedError

    @abstractmethod
    def get_open_interest(self, symbol: str, start: datetime, end: datetime):
        raise NotImplementedError
