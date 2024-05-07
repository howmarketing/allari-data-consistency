from dataclasses import dataclass
from src.lib.database.migration.models.db import *

@dataclass
class BaseModel(Model):
    class Meta:
        database = db