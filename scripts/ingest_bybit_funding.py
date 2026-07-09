#!/usr/bin/env python3
"""CLI: fetch Bybit funding-rate history and write it to TimescaleDB.

Usage:
    uv run python scripts/ingest_bybit_funding.py \\
        --symbol BTCUSDT --start 2024-01-01 --end 2024-01-02

No trading functionality. This script only fetches and stores data.
"""

import argparse
from datetime import datetime, timezone

from backend.data.adapters.bybit import BybitExchange
from backend.data.storage.timescale_writer import TimescaleWriter


def _parse_utc_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    parser.add_argument("--start", required=True, type=_parse_utc_date, help="YYYY-MM-DD, UTC")
    parser.add_argument("--end", required=True, type=_parse_utc_date, help="YYYY-MM-DD, UTC")
    args = parser.parse_args()

    exchange = BybitExchange()
    records = exchange.get_funding(args.symbol, args.start, args.end)

    writer = TimescaleWriter()
    try:
        written = writer.write_funding(records)
    finally:
        writer.close()

    print(f"fetched={len(records)} written={written}")


if __name__ == "__main__":
    main()
