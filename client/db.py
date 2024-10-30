from peewee import CharField, FloatField, IntegerField, Model, SqliteDatabase

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class Data(BaseModel):
    ticker = CharField(max_length=3)
    price = FloatField()
    timestamp = IntegerField()
