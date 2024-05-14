# %%
from peewee import *
from random import randint
from typing import Any, Callable, TypeVar
import json

# %%
T = TypeVar('T')

# %%
def pad_start(width, fillchar, number) -> int:
    return int(str(number).rjust(width, fillchar))

def pad_end(width, fillchar, number) -> int:
    return int(str(number).ljust(width, fillchar))

# %%

def get_random_integer(min_value: T = 1, max_value: T = 9) -> int:
    min = pad_start(7,'1', pad_end(6, '0', min_value))
    max = pad_start(8, '9', pad_end(7, '9', max_value))
    return randint(min, max)

rand_number = get_random_integer()

print(rand_number)

# %%
database_name = 'notebooks_2_{}.db'.format(get_random_integer())
print(database_name)

# %%
db = SqliteDatabase(database_name)

# %%
# dir(db)

# %%
db.connection();

# %%
class BaseModel(Model):
    class Meta:
        database = db

# %%
class Person(BaseModel):
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    phone = CharField(null=True)
    
class Experience(BaseModel):
    id = AutoField()
    title = CharField()
    company = CharField()
    start_date = DateField()
    end_date = DateField(null=True)
    person = ForeignKeyField(Person, backref='experiences')
    
class Contact(BaseModel):
    id = AutoField()
    nickname = CharField()
    owner = ForeignKeyField(Person, backref='contacts')

class Phone(BaseModel):
    id = AutoField()
    type = CharField()
    number = CharField()
    contact = ForeignKeyField(Contact, backref='phones')


# %%
db.create_tables([Person, Experience, Contact, Phone])

# %%
data = {
    'person_record': {
        'first_name': 'Gabriel',
        'last_name': 'Ariza',
        'phone': '1234567890'
    },
    'experience_records': [
        {
            'title'      :      'Developer',
            'company'    :      'Google',
            'start_date' :      '2018-01-01',
            'end_date'   :      '2018-02-01',
            'person_id'     :      0
        }
    ],
    'contact_records': [
        {
            'nickname': 'john_doe',
            'owner_id': 0
        }
    ],

    'phone_records': [
        {
            'type': 'home',
            'number': '1234567890',
            'contact_id': 0
        }
    ]
}


# %%
insert_data = data.get('person_record', {})
print(json.dumps([insert_data], indent=4))

# %%
insert_response = Person.create(**insert_data)
print(json.dumps([insert_response.__data__], indent=4))
# dir(insert_response)

# %%
insert_data = data.get('person_record', {})
insert_data['experiences'] = data.get('experience_records', [])
insert_data['contacts'] = data.get('contact_records', [])
for i, contact in enumerate(insert_data['contacts']):
    contact.update({'nickname': '{}. {}'.format((i + 1), contact.get('nickname', ''))})
    contact['phones'] = data.get('phone_records', [])

print(json.dumps([insert_data], indent=4))

# %%
# The create method should insert the person record into the database
insert_response = Person.create(**insert_data)

# %%
print(type(insert_response)) # Should to be the class model: Person <Model: Person>
print(insert_response) # Should to output the person primary key (id) value (2)
print(insert_response.id) # Should be the same value as above as the both are outputting the primary key (id) value (2)

# %%
print(json.dumps([insert_response.__data__], indent=2))

# %%
print(json.dumps([insert_response.experiences], indent=2))

# %%
for exp in insert_response.experiences:
    exp.update({'person_id': insert_response.id})

# %%
print(json.dumps(insert_response.experiences, indent=2))

# %%
print(json.dumps(insert_response.contacts, indent=4))

# %%
for contact in insert_response.contacts:
    contact.update({'owner_id': insert_response.id})

# %%
print(json.dumps(insert_response.contacts, indent=4))

# %%
experiencesEntity: list[Experience] = []
for index, exp in enumerate(insert_response.experiences):
    experiencesEntity.append(Experience(**exp))

# %%
print(type(experiencesEntity[0]))

# %%
print(type(experiencesEntity[0].person))

# %%
print(json.dumps([experiencesEntity[0].person.__data__], indent=4))

# %%
contactsEntity: list[Contact] = []
for index, contact in enumerate(insert_response.contacts):
    contactsEntity.append(Contact(**contact))

# %%
print(type(contactsEntity[0]))

# %%
print(type(contactsEntity[0].owner))

# %%

try:
    insert_response.__data__['experiences'] = insert_response.experiences
    insert_response.__data__['contacts'] = insert_response.contacts
except Exception as e:
    print(e)

print(json.dumps([insert_response.__data__], indent=4))
dir(insert_response)

# %%

dir(insert_response.__data__)

# %%
print(json.dumps([{'{}'.format(i):d} for i, d in insert_response.__data__.items()], indent=2))

# %%
print(json.dumps(insert_response.experiences, indent=4))

# %%
print(json.dumps(insert_response.contacts, indent=4))

# %%
print(insert_response.id)

# %%
experiences = Experience().select() # no experience records should exist at this moment

# %%
print([exp for exp in experiences]) # Should output an empty array

# %%
insert_response.experiences = experiencesEntity
insert_response.contacts = contactsEntity

# %%
print(insert_response.experiences[0].person.first_name)
print(insert_response.contacts[0].owner.first_name)

# %%
experience_bulk_create = Experience.bulk_create(insert_response.experiences)

# %%
experiences = Experience().select() # The person experiences should be retrived

# %%
print(len(experiences) )

# %%
contacts_bulk_create = Contact.bulk_create(insert_response.contacts)

# %%
contacts = Contact.select() # The person contacts should be retrived

# %%
print(len(contacts))

# %%
print(len(insert_response.contacts[0].phones))
print(len(contacts[0].phones))

# %%
print(insert_response.contacts[0].save())

# %%
print(insert_response.contacts[0].id)
print(insert_response.contacts[0].nickname)
print(insert_response.contacts[0].phones[0])


# %%
db.close()

# %%



