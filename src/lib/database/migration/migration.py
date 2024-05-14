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


class FindContactsByPersonId:
    
    __query = ""
    __query_result = []
    person_id = 0
    
    def __init__(self, person_id):
        self.person_id = person_id
    
    def set_query(self, show_only_contacts_matching_person = False):
        self.__query = ""
        self.__query +=  "SELECT "
        self.__query +=      "phone.id, "
        self.__query +=      "person.first_name || ' ' || person.last_name AS 'contact_owner_name', "
        self.__query +=      "contact.nickname, "
        self.__query +=      "phone.type, "
        self.__query +=      "phone.number, "
        self.__query +=      "phone.contact_id, "
        self.__query +=      "phone_number_person.id, "
        self.__query +=      "phone_number_person.first_name || ' ' || phone_number_person.last_name AS 'contact_person_name' "
        self.__query +=  "FROM "
        self.__query +=      "person "
        self.__query +=  "JOIN "
        self.__query +=      "contact ON person.id = contact.owner_id AND contact.owner_id = ? "
        self.__query +=  "JOIN "
        self.__query +=      "phone ON phone.contact_id = contact.id "
        if(show_only_contacts_matching_person):
            self.__query +=  "JOIN "
        else:
            self.__query +=  "LEFT JOIN "
        
        self.__query +=      "person as phone_number_person ON phone_number_person.phone LIKE phone.number "
        self.__query +=  "WHERE "
        self.__query +=      "person.id = ? "
        self.__query +=  "ORDER BY "
        self.__query +=      "person.id, phone.contact_id ASC"
    
    def execute_query(self):
        
        cursor = db.execute_sql('{}'.format(self.__query), (self.person_id, self.person_id))
        for value in cursor:
            id, contact_owner_name, nickname, type, number, contact_id, id, contact_person_name = value
            data = {
                'id'                    :       id,
                'contact_owner_name'    :       contact_owner_name,
                'nickname'              :       nickname,
                'type'                  :       type,
                'number'                :       number,
                'contact_id'            :       contact_id,
                'id'                    :       id,
                'contact_person_name'   :       contact_person_name
            }
            self.__query_result.append(data)
        return self.__query_result
    
    def get_query_result(self, show_only_contacts_matching_person = False):
        self.set_query(show_only_contacts_matching_person)
        self.execute_query()
        return self.__query_result
    

class FindExperiences:
    
    def get_experiences_by_person_id(self, person_id):
        return Experience.select().where(Experience.person == person_id)
    
    # Get experiences where company name contains company_name and person_id is not equal person_id
    def get_experiences_where_company_name_like(self, company_name, person_id=0):
        return Experience.select().where(Experience.company.contains(company_name) & (Experience.person != person_id))

    # This function retrieves experiences from the database where the company name contains the given string,
    # the person_id does not match the given person_id, and the start and end dates fall within the given range.
    # Additionally, it checks that the duration between the start and end dates is at least 90 days.
    # Parameters:
    # company_name (str): The company name to search for.
    # person_id (int, optional): The person_id to exclude from the search. Defaults to 0.
    # start_date (datetime.date, optional): The start date of the range. Defaults to None.
    # end_date (datetime.date, optional): The end date of the range. Defaults to None.
    # Returns:
    # peewee.ModelSelect: A query object containing the matching experiences.
    def get_experiences_where_company_name_like_not_person_id_dates_between_old(self, company_name, person_id=0, start_date=None, end_date=None):
        if end_date is None:
            end_date = datetime.date.today()
        return Experience.select().where(
            Experience.company.contains(company_name) &
            (Experience.person != person_id) &
            (Experience.start_date <= start_date) &
            (Experience.end_date >= start_date) &
            (Experience.start_date <= end_date) &
            (Experience.end_date >= end_date)
        )


    def get_experiences_where_company_name_like_not_person_id_dates_between(self, company_name, person_id=0, start_date=None, end_date=None):
        return Experience.select().where(
            (
                Experience.company.contains(company_name) &
                (Experience.person != person_id) &
                (Experience.start_date <= start_date) &
                (Experience.end_date >= start_date) &
                (Experience.start_date <= end_date) &
                (Experience.end_date >= end_date) &
                (SQL('JULIANDAY(end_date) - JULIANDAY(start_date)') >= 90) &
                (SQL('JULIANDAY({}) - JULIANDAY(start_date)'.format(end_date)) >= 90)
            )
        )



        
PERSON_ID = 1

def migrate_database():
    migration = Migration()
    # find_contacts_by_person_id = FindContactsByPersonId(PERSON_ID)
    # person_contacts = find_contacts_by_person_id.get_query_result()
    person_contacts = FindContactsByPersonId(PERSON_ID).get_query_result()
    
    print(person_contacts)
    
    
    return
    
    
    
    
    
    
    
    
    
    
    find_experiences = FindExperiences()
    person_experiences:list[Experience] = find_experiences.get_experiences_by_person_id(PERSON_ID)
    persons_data = migration.get_person_data()
    contacts_data = migration.get_person_data()
    
    
    print('Contacts:')
    print(json.dumps(person_contacts, indent=2))
 
    others_experiences: list(Experience) = []
    
    print('Experiences:')
    for exp in person_experiences:
        print('Experience:')
        exp.__data__.update({'start_date': str(exp.start_date)})
        exp.__data__.update({'end_date': str(exp.start_date)})
        print(json.dumps([exp.__data__], indent=2))
        
        others_experience:list[Experience] = find_experiences.get_experiences_where_company_name_like_not_person_id_dates_between_old(
            company_name=exp.company,
            person_id=PERSON_ID,
            start_date=exp.start_date,
            end_date=exp.end_date,
        )
        print('Others experiences matching:')
        for other_experience in others_experience:
            others_experiences.append(other_experience.__data__)
            print(other_experience.__data__)
    
    print('ALL others_experiences')
    print(others_experiences)
    
    
            
    
        
        
