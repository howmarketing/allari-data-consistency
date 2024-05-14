import json
import datetime
from peewee import SQL

# Import necessary modules and models
from src.lib.database.conn import db, database_connect, is_database_connected
from src.lib.database.migration.models.person_model import Person
from src.lib.database.migration.models.experience_model import Experience
from src.lib.database.migration.models.contact_model import Contact
from src.lib.database.migration.models.phone_model import Phone
from src.lib.helpers.format import normalize_phone

# Define file paths for JSON data
FILES = {
    'person_records'    : 'src/lib/database/migration/data/persons.json',
    'contact_records'   : 'src/lib/database/migration/data/contacts.json'
}


class Migration:
    
    # private property persons data
    _persons_data = []
    
    # private property contacts data
    _contacts_data = []
    
    # Constructor
    def __init__(self):
        self.database_connect()
        try:
            self.migrate_tables()
        except Exception as e:
            msg = 'Database migration could not be completed: {}'.format(e)
            print(msg)
            raise Exception(msg)

        self.load_persons_json_file_data()
        self.load_contacts_json_file_data()
        self.consolidate_persons_data()
        self.consolidate_contacts_data()
        self.create_person_records()
        self.create_contact_records()
    
    def get_person_data(self):
        return self._persons_data

    def get_contacts_data(self):
        return self._persons_data
    
    
    # Method to connect to the database
    def database_connect(self):
        if not is_database_connected():
            database_connect()

    def migrate_tables(self):
        try:
            db.create_tables([Person, Experience, Contact, Phone])
        except Exception as e:
            msg = 'Database migration could not be completed: {}'.format(e)
            print(msg)
            raise Exception(msg)
    # Method to create database tables
    def create_tables():
        try:
            db.create_tables([Person, Experience, Contact, Phone])
        except Exception as e:
            msg = 'Database migration could not be completed: {}'.format(e)
            print(msg)
            raise Exception(msg)
    
    # Method to load JSON data from a file
    def load_json_file_data(self, file_key):
        file = FILES.get(file_key, None)
        if file is None:
            msg = 'load_json_data({}): File could not be found'.format(file_key)
            print(msg)
            raise Exception(msg)
        
        with open(file, 'r') as f:
            try:
                records = json.load(f)
                return records
            except Exception as e:
                msg = 'load_json_data({}): File could not be loaded: {}'.format(file_key, e)
                print(msg)
                raise Exception(msg)
    
    # Method to load persons data from JSON file
    def load_persons_json_file_data(self):
        self._persons_data = self.load_json_file_data('person_records')
    
    # Method to load contacts data from json file
    def load_contacts_json_file_data(self):
        self._contacts_data = self.load_json_file_data('contact_records')
    
    # Method to consolidate persons data
    def consolidate_persons_data(self):
        consolidated_data = []
        for person in self._persons_data:
            consolidated_person = {
                'first_name': person['first'],
                'last_name': person['last'],
                'phone': normalize_phone(person['phone']),
                'experiences': [{'person_id':0, 'company': exp['company'], 'title': exp['title'], 'start_date': exp['start'], 'end_date': exp['end']} for exp in person['experience']]
                 
            }
            consolidated_data.append(consolidated_person)
        self._persons_data = consolidated_data
    
    # Method to consolidate contacts data
    def consolidate_contacts_data(self):
        consolidated_data = []
        for contact in self._contacts_data:
            consolidated_contact = {
                'owner_id': contact['owner_id'],
                'nickname': contact['contact_nickname'],
                'phones': [{'type': phone['type'], 'number': normalize_phone(phone['number'])} for phone in contact['phone']],
            }
            consolidated_data.append(consolidated_contact)
        self._contacts_data = consolidated_data
    
    def create_person_records(self):
        for person in self._persons_data:
            personEntity = Person.create(**person)
            for exp in person['experiences']:
                exp['person_id'] = personEntity.id
                Experience.create(**exp)
    
    def create_contact_records(self):
        for contact in self._contacts_data:
            contactEntity = Contact.create(**contact)
            for phone in contact['phones']:
                phone['contact_id'] = contactEntity.id
                Phone.create(**phone)

