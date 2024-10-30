from peewee import SqliteDatabase

from client.db import Data
import pytest

db = SqliteDatabase("test_db.db")


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    if db.is_closed():
        db.connect()

    db.create_tables([Data])

    yield

    db.drop_tables([Data])
    db.close()
