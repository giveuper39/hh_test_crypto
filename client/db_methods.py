from db import Data
from peewee import SqliteDatabase


def init_db(db: SqliteDatabase) -> None:
    """Connect to the database and create the tables.

    :param db: SqliteDatabase instance
    :return:
    """
    db.connect()
    db.create_tables([Data])
    db.close()


def insert_price(ticker: str, price: float, timestamp: int, db: SqliteDatabase) -> None:
    """Insert a new price into the database.

    :param ticker: Currency ticker (e.g. 'btc', 'eth')
    :param price: Currency price
    :param timestamp: Current UNIX timestamp
    :param db: SqliteDatabase instance
    :return:
    """
    with db.atomic():
        Data.create(ticker=ticker, price=price, timestamp=timestamp)
