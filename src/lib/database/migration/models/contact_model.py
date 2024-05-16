"""Module providing a Contact entity class."""
from peewee import CharField, AutoField, ForeignKeyField
from src.lib.database.migration.models.base_model import BaseModel
from src.lib.database.migration.models.person_model import Person

class Contact(BaseModel):
    """
    Represents a contact associated with a person in the database.
    
    The `Contact` model has the following fields:
    - `id`: A unique identifier for the contact.
    - `nickname`: The nickname or alias of the contact.
    - `owner`: A foreign key reference to the `Person` model that owns this contact.
    """
    id = AutoField()
    nickname = CharField()
    owner = ForeignKeyField(Person, backref='contacts')
