from peewee import CharField, AutoField
from src.lib.database.migration.models.base_model import BaseModel

class Person(BaseModel):
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    phone = CharField(null=True)
