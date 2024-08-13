"""Module providing a Experience entity class."""
from peewee import CharField, AutoField, DateField, ForeignKeyField
from src.lib.database.migration.models.base_model import BaseModel
from src.lib.database.migration.models.person_model import Person

class Experience(BaseModel):
    """
    Represents an experience record for a person, such as a job or internship.
    
    Attributes:
        id (int): The unique identifier for the experience record.
        title (str): The title of the experience, such as the job title.
        company (str): The name of the company or organization where the experience took place.
        start_date (datetime.date): The date the experience started.
        end_date (datetime.date): The date the experience ended, or None if the experience is ongoing.
        person (Person): The person associated with this experience record.
    """
    id = AutoField()
    title = CharField()
    company = CharField()
    start_date = DateField()
    end_date = DateField(null=True)
    person = ForeignKeyField(Person, backref='experiences')
