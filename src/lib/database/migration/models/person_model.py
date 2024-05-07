from dataclasses import dataclass
from base_model import *

@dataclass
class Person(BaseModel):
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    phone = CharField(null=True)
