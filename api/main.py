from __future__ import annotations

import time
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Query

from client.db import Data, db

app = FastAPI()


def timestamp_to_str(timestamp: int) -> str:
    """Convert UNIX Timestamp to datetime string.

    :param timestamp: UNIX Timestamp
    :return: String representation of UNIX Timestamp in format 'DD-MM-YYYY HH:MM:SS'
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%d-%m-%Y %H:%M:%S")


@app.get("/crypto/all")
def get_all_prices(ticker: str = Query(..., description="Value ticker (e.g. 'btc' or 'eth')")) -> list[dict]:
    """Get all prices for certain cryptocurrency (by 'ticker' query parameter).

    :param ticker: Cryptocurrency ticker (e.g. 'btc' or 'eth')
    :return: List of dictionaries with 'ticker', 'price' and 'timestamp' keys
    """
    with db.atomic():
        prices: list[Data] = Data.select().where(Data.ticker == ticker)
        if not prices:
            raise HTTPException(status_code=404, detail="No data found by this ticker")
        return [{"ticker": ticker, "price": p.price, "timestamp": timestamp_to_str(p.timestamp)} for p in prices]


@app.get("/crypto/latest")
def get_latest_price(ticker: str = Query(..., description="Value ticker (e.g. 'btc' or 'eth')")) -> dict:
    """Get the latest price for certain cryptocurrency (by 'ticker' query parameter).

    :param ticker: Cryptocurrency ticker (e.g. 'btc' or 'eth')
    :return: Dictionary with 'ticker', 'price' and 'timestamp' keys
    """
    with db.atomic():
        price: list[Data] = Data.select().where(Data.ticker == ticker).order_by(Data.timestamp.desc()).limit(1)
        if not price:
            raise HTTPException(status_code=404, detail="No data found by this ticker")
        return {"ticker": ticker, "price": price[0].price, "timestamp": timestamp_to_str(price[0].timestamp)}


@app.get("/crypto/date")
def get_price_by_date(
    ticker: str = Query(..., description="Value ticker (e.g. 'btc' or 'eth')"),
    start: str | None = Query(None, description="Start date (DD-MM-YYYY)"),
    end: str | None = Query(None, description="End date (DD-MM-YYYY)"),
) -> list[dict]:
    """Get prices for certain cryptocurrency (by 'ticker' query parameter) from start date till end date.

    :param ticker: Cryptocurrency ticker (e.g. 'btc' or 'eth')
    :param start: Start date (DD-MM-YYYY)
    :param end: End date (DD-MM-YYYY)
    :return: List of dictionaries with 'ticker', 'price' and 'timestamp' keys
    """
    try:
        start_timestamp = (
            time.mktime(datetime.strptime(start, "%d-%m-%Y").replace(tzinfo=timezone.utc).timetuple()) if start else 0
        )
        end_timestamp = (
            time.mktime(datetime.strptime(end, "%d-%m-%Y").replace(tzinfo=timezone.utc).timetuple())
            if end
            else int(time.time())
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid start and/or end date format")
    with db.atomic():
        prices: list[Data] = (
            Data.select()
            .where((Data.ticker == ticker) & (Data.timestamp >= start_timestamp) & (Data.timestamp <= end_timestamp))
            .order_by(Data.timestamp)
        )
        if not prices:
            raise HTTPException(status_code=404, detail="No data found by this ticker or start/end dates")
        return [{"ticker": ticker, "price": p.price, "timestamp": timestamp_to_str(p.timestamp)} for p in prices]
