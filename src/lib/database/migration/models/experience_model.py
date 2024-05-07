from dataclasses import dataclass
from base_model import *
from person_model import Person

@dataclass
class Experience(BaseModel):
    id = AutoField()
    title = CharField()
    company = CharField()
    start_date = DateField()
    end_date = DateField(null=True)
    person = ForeignKeyField(Person, backref='experiences')