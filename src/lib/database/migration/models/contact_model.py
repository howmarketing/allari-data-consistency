from peewee import CharField, AutoField, ForeignKeyField
from src.lib.database.migration.models.base_model import BaseModel
from src.lib.database.migration.models.person_model import Person

class Contact(BaseModel):
    id = AutoField()
    nickname = CharField()
    owner = ForeignKeyField(Person, backref='contacts')