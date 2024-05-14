from peewee import CharField, AutoField, DateField, ForeignKeyField
from src.lib.database.migration.models.base_model import BaseModel
from src.lib.database.migration.models.person_model import Person

class Experience(BaseModel):
    id = AutoField()
    title = CharField()
    company = CharField()
    start_date = DateField()
    end_date = DateField(null=True)
    person = ForeignKeyField(Person, backref='experiences')







