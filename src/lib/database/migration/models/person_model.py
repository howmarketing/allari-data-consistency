"""Module providing a Person entity class."""

from peewee import CharField, AutoField
from src.lib.database.migration.models.base_model import BaseModel

class Person(BaseModel):
    """
    Represents a person in the database.
    
    Attributes:
        id (int): The unique identifier for the person.
        first_name (str): The person's first name.
        last_name (str): The person's last name.
        phone (str, optional): The person's phone number.
    """
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    phone = CharField(null=True)
