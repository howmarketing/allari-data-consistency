"""Module providing a Phone entity class."""
from peewee import CharField, AutoField, ForeignKeyField
from src.lib.database.migration.models.base_model import BaseModel
from src.lib.database.migration.models.contact_model import Contact

class Phone(BaseModel):
    """
    Represents a phone number associated with a contact.
    
    Attributes:
        id (int): The unique identifier for the phone number.
        type (str): The type of phone number (e.g. "mobile", "home", "work").
        number (str): The actual phone number.
        contact (Contact): The contact that this phone number is associated with.
    """
    id = AutoField()
    type = CharField()
    number = CharField()
    contact = ForeignKeyField(Contact, backref='phones')