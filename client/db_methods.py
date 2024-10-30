from db import Data, db


def init_db() -> None:
    """Connect to the database and create the tables.

    :return:
    """
    db.connect()
    db.create_tables([Data], safe=True)
    db.close()


def insert_price(ticker: str, price: float, timestamp: int) -> None:
    """Insert a new price into the database.

    :param ticker: Currency ticker (e.g. 'btc', 'eth')
    :param price: Currency price
    :param timestamp: Current UNIX timestamp
    :return:
    """
    db.connect()
    Data.create(ticker=ticker, price=price, timestamp=timestamp)
    db.close()
