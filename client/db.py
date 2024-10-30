from os import getenv

from dotenv import load_dotenv
from peewee import CharField, FloatField, IntegerField, Model, SqliteDatabase

load_dotenv()

DB_NAME = getenv("DB_NAME")
main_db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    class Meta:
        database = main_db


class Data(BaseModel):
    ticker = CharField(max_length=3)
    price = FloatField()
    timestamp = IntegerField()
