import asyncio
import logging
import sys
import time

import aiohttp
from db import main_db
from db_methods import init_db, insert_price
from peewee import SqliteDatabase


async def gather_price(url: str, session: aiohttp.ClientSession, index: str, db: SqliteDatabase = main_db) -> None:
    """Gather the price of particular index and save it to database.

    :param db: SqliteDatabase instance
    :param url: API URL
    :param session: aiohttp ClientSession object
    :param index: Cryptocurrency index (e.g. 'btc_usd', 'eth_usd')
    :return:
    """
    params = {"index_name": index}
    try:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:  # noqa: PLR2004
                logging.error("Response status is not OK")
                return
            data = await resp.json()
            if data["result"]:
                price = data["result"]["index_price"]
                timestamp = int(time.time())
                insert_price(index[:3], price, timestamp, db)
    except Exception as e:
        logging.exception(e)


async def main() -> None:
    """Client main loop.

    :return:
    """
    init_db(main_db)
    url = "https://www.deribit.com/api/v2/public/get_index_price"
    indexes = ("btc_usd", "eth_usd")
    try:
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = (gather_price(url, session, index) for index in indexes)
                await asyncio.gather(*tasks)
                await asyncio.sleep(60)
    except aiohttp.ClientError as err:
        logging.exception(err)
        return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
