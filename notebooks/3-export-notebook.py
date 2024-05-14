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
database_name = 'notebooks_3_{}.db'.format(get_random_integer())
print(database_name)

# %%
# db = SqliteDatabase(database_name, pragmas={'journal_mode':'wal','foreing_keys':1})
db = SqliteDatabase(database_name, pragmas={'foreing_keys':1})

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
    expEntity = Experience(**exp)
    expEntity.save()
    experiencesEntity.append(expEntity)

# %%
print(type(experiencesEntity[0]))

# %%
print(type(experiencesEntity[0].person))

# %%
print(json.dumps([experiencesEntity[0].person.__data__], indent=4))

# %%
contactsEntity: list[Contact] = []
for index, contact in enumerate(insert_response.contacts):
    contactEntity = Contact(**contact)
    contactEntity.save()
    contactsEntity.append(contactEntity)

# %%
lent_contactsEntity = len(contactsEntity)

# %%
print(lent_contactsEntity)

# %%
print(type(contactsEntity[0]) if lent_contactsEntity >= 1 else 'no contacts')

# %%
print(type(contactsEntity[0].owner) if lent_contactsEntity >= 1 else 'no contact to access his owner')

# %%
print(type(contactsEntity[0].phones) if lent_contactsEntity >= 1 else 'no contact to access his phones')

# %%
print(json.dumps(insert_response.contacts, indent=2))

# %%
print(json.dumps(contactsEntity[0].phones, indent=2))

# %%
print(contactsEntity[0].id)

# %%

for c in contactsEntity:
    phone_entity_list:list[Phone] = []
    for p in c.phones:
        p.update({'contact_id': c.id})
        phoneEntity = Phone(**p)
        phoneEntity.save()
        phone_entity_list.append(phoneEntity)
    # update the contact phones with the phone_entity_list
    # c.update({'phones': phone_entity_list})
    c.phones = phone_entity_list
    

# %%
phones = []
for c in contactsEntity:
    for p in c.phones:
        phones.append(p.__data__)

print(json.dumps(phones, indent=2))

# %%
contactsEntity[0].phones[0].__data__

# %%
contactsEntity[0].phones[0].contact.__data__

# %%
contactsEntity[0].phones[0].contact.owner.__data__

# %%
contactsEntity[0].phones[0].contact.owner.experiences[0].__data__

# %%
phone_contact_owner_experience_list = []
for phone_contact_owner_experience in contactsEntity[0].phones[0].contact.owner.experiences:
    phone_contact_owner_experience.__data__.update({'start_date': phone_contact_owner_experience.__data__['start_date'].__str__()})
    phone_contact_owner_experience.__data__.update({'end_date': phone_contact_owner_experience.__data__['end_date'].__str__()})
    phone_contact_owner_experience_list.append(phone_contact_owner_experience.__data__)
# print(json.dumps(phone_contact_owner_experience_list, indent=2))
print(json.dumps(phone_contact_owner_experience_list, indent=2))

# %%
insert_response.experiences = experiencesEntity
insert_response.contacts = contactsEntity

# %%
print(insert_response.experiences[0].person.first_name)
print(insert_response.contacts[0].owner.first_name)

# %%

try:
    insert_response.__data__['experiences'] = insert_response.experiences
    insert_response.__data__['contacts'] = insert_response.contacts
except Exception as e:
    print(e)



# %%
print([insert_response])

# %%
print(insert_response.experiences)

# %%
print(insert_response.contacts)

# %%
print(insert_response.contacts[0].phones)

# %%
for k,v in insert_response.__data__.items():
    print(k,': ',v)

# %%
experiences = Experience().select()

# %%
print([exp for exp in experiences])

# %%
contacts = Contact.select() # The person contacts should be retrived

# %%
print([c for c in contacts])

# %%
print(len(insert_response.contacts[0].phones))
print(len(contacts[0].phones))

# %%
print(insert_response.contacts[0].nickname)
print(insert_response.contacts[0].phones[0].number)

# %%
db.close()


