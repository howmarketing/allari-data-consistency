"""Module providing a Contact entity class."""
from peewee import Model
from src.lib.database.migration.models.db import db

class BaseModel(Model):
    """
    Base class for all database models. Provides a common database connection
    for all models.
    """
    class Meta:
        """
        The `Meta` class is a nested class within the `BaseModel` class that provides 
        configuration options for the model. The `database` attribute specifies the database connection 
        to use for the model, which is set to the `db` variable 
        from the `src.lib.database.migration.models.db` module.
        """
        database = db
