from peewee import Model
from src.lib.database.migration.models.db import db

class BaseModel(Model):
    class Meta:
        database = db
