from datetime import datetime

import aiohttp
import pytest
from aioresponses import aioresponses


from client.db import Data
from client.db_methods import insert_price
from client.main import gather_price
from tests.conftest import db

@pytest.fixture
def mock_price_response():
    return {
        "jsonrpc": "2.0",
        "result": {"index_price": 71850.85, "estimated_delivery_price": 71850.85},
        "usIn": 1730316609257355,
        "usOut": 1730316609257502,
        "usDiff": 147,
        "testnet": False,
    }


@pytest.mark.asyncio
async def test_insert_price():
    index = "btc_usd"
    ticker = index[:3]
    price = 11628.81
    timestamp = int(datetime.now().timestamp())

    insert_price(ticker, price, timestamp, db)

    stored_price = Data.get(Data.ticker == ticker)
    assert stored_price.ticker == ticker
    assert stored_price.price == price
    assert stored_price.timestamp == timestamp


@pytest.mark.asyncio
async def test_gather_price(mock_price_response):
    index = "btc_usd"
    ticker = index[:3]
    url = "https://www.deribit.com/api/v2/public/get_index_price"

    with aioresponses() as m:
        m.get(f"{url}?index_name={index}", payload=mock_price_response)

        async with aiohttp.ClientSession() as session:
            await gather_price(url, session, index)

    stored_price = Data.get(Data.ticker == ticker)
    assert stored_price.ticker == ticker
    assert stored_price.price == mock_price_response["result"]["index_price"]
