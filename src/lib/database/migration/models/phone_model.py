from peewee import CharField, AutoField, ForeignKeyField
from src.lib.database.migration.models.base_model import BaseModel
from src.lib.database.migration.models.contact_model import Contact

class Phone(BaseModel):
    id = AutoField()
    type = CharField()
    number = CharField()
    contact = ForeignKeyField(Contact, backref='phones')