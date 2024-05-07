from dataclasses import dataclass
from base_model import *
from person_model import Person

@dataclass
class Contact(BaseModel):
    id = AutoField()
    nickname = CharField()
    owner = ForeignKeyField(Person, backref='contacts')
