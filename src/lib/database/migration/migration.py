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
    __person_id = 0
    
    def __init__(self, person_id):
        self.__person_id              = person_id
        self.__query                =       ""
        self.__query_result         =       []
    
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
        self.__query_result = []
        cursor = db.execute_sql('{}'.format(self.__query), (self.__person_id, self.__person_id))
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
    

class FindExperiencesWithPermanenceDays:
    
    __query = ""
    __query_result = []
    
    company_name           =      ''
    min_permanence_days    =      90
    person_id              =      00
    start_date             =      None
    end_date               =      None
    
    def __init__(self, company_name='', start_date = None, end_date = None, min_permanence_days = 90, person_id = 0):
        
        self.company_name           =       company_name
        self.min_permanence_days    =       min_permanence_days
        self.person_id              =       person_id
        self.start_date             =       datetime.date.today() - datetime.timedelta(days=min_permanence_days+1) if start_date is None else datetime.date.fromisoformat(str(start_date))
        self.end_date               =       datetime.date.today() if end_date is None else datetime.date.fromisoformat(str(end_date))
        self.start_date             =       str(self.start_date)
        self.end_date               =       str(self.end_date)
        self.__query                =       ""
        self.__query_result         =       []
    
    def date_range_gte_min_perm(self, start_date, end_date):        
        return (datetime.date.fromisoformat(str(end_date)) - datetime.date.fromisoformat(str(start_date))).days >= self.min_permanence_days
    
    def set_query(self):
        self.__query = ""
        self.__query +=    "SELECT  "
        self.__query +=        "e.id, "
        self.__query +=        "e.person_id, "
        self.__query +=        "e.company, "
        self.__query +=        "e.title, "
        self.__query +=        "(JULIANDAY(COALESCE(end_date, CURRENT_DATE)) - JULIANDAY(start_date)) as 'permanence_days', "
        self.__query +=        "e.start_date, "
        self.__query +=        "e.end_date "
        self.__query +=    "FROM  "
        self.__query +=        "experience as e "
        self.__query +=    "WHERE "
        self.__query +=        "e.company like ? "
        self.__query +=    "AND "
        self.__query +=        "permanence_days >= ? "
        self.__query +=    "AND "
        self.__query +=        "person_id <> ? "
        self.__query +=    "AND "
        self.__query +=        "start_date <= ? " # start_date lte (self.end_date - self.min_permanence_days)
        self.__query +=     "ORDER BY "
        self.__query +=         "e.id, e.person_id ASC"
    
    def get_query_binds(self):
        company = "%{}%".format(self.company_name)
        permanence_days = int(self.min_permanence_days)
        person_id = int(self.person_id)
        start_date = datetime.date.fromisoformat(str(self.end_date)) - datetime.timedelta(days=permanence_days)
        start_date = str(start_date)
        return (company, permanence_days, person_id, start_date)
    
    def execute_query(self):
        date_range_is_valid = self.date_range_gte_min_perm(self.start_date, self.end_date)
        if not date_range_is_valid:
            print('Invalid date range of {}, {} is not gte {} days'. format(self.start_date, self.end_date, self.min_permanence_days))
            return []
        binds = self.get_query_binds()
        query = '{}'.format(self.__query)

        cursor = db.execute_sql(query, binds)
        
        for value in cursor:
            id, person_id, company, title, permanence_days, start_date, end_date = value
            data = {
                'id'                    :       id,
                'person_id'             :       person_id,
                'company'               :       company,
                'title'                 :       title,
                'permanence_days'       :       permanence_days,
                'start_date'            :       start_date,
                'end_date'              :       end_date
            }
            self.__query_result.append(data)
        return self.__query_result
    
    def get_query_result(self):
        self.set_query()
        self.execute_query()
        return self.__query_result
    
    def __repr__(self):
        l = [7, 0, 10, 9, 11]
        print('company_name'         ,  ': ', ' '*l[0]      ,    self.company_name)
        print('min_permanence_days'  ,  ': ', ' '*l[1]      ,    self.min_permanence_days)
        print('person_id'            ,  ': ', ' '*l[2]      ,    self.person_id)
        print('start_date'           ,  ': ', ' '*l[3]      ,    self.start_date)
        print('end_date'             ,  ': ', ' '*l[4]      ,    self.end_date)
        print('query_results'        ,  ': ', ' '*l[4]      ,    self.__query_result)
                
        return list((self.company_name, self.min_permanence_days, self.person_id, self.start_date, self.end_date, self.__query_result))



class RelatedExperiencesFromExperience():
    
    _related_from_experiences:list[Experience] = []
    _person_id = 0
    _person:Person = None
    
    def __init__(self, person_id = 0):
        self._related_from_experiences = []
        self._person_id = person_id        

    def set_person_by_id(self, person_id=None):
        if person_id is None:
            person_id = self._person_id
        if self._person is not None and self._person.id == person_id:
            return self
        
        self._person = Person.get_by_id(self._person_id)
        return self
    
    def get_person_by_id(self, person_id=None) -> Person:
        if person_id is None:
            person_id = self._person_id
        return self.set_person_by_id(person_id=person_id)._person
    
    def get_person_experiences_by_person_id(self, person_id=None) -> list[Experience]:
        if person_id is None:
            person_id = self._person_id
        person = self.get_person_by_id(person_id=person_id)
        return person.experiences
    
    
    def set_related_experiences_from_person_experiences(self, person_id=None, min_permanence_days=90) -> list[Experience]:
        if person_id is None:
            person_id = self._person_id

        self._related_from_experiences = []
        
        person_exp = self.get_person_experiences_by_person_id(person_id)
        
        for exp in person_exp:
            find_experiences_with_permanence_days = FindExperiencesWithPermanenceDays(
                company_name=exp.company,
                start_date=exp.start_date,
                end_date=exp.end_date,
                min_permanence_days=min_permanence_days,
                person_id=exp.person.id
            )
            related_by_experience = find_experiences_with_permanence_days.get_query_result()
            for related in related_by_experience:
                self._related_from_experiences.append(Experience(
                    person=related['person_id'],
                    company=related['company'],
                    title=related['title'],
                    start_date=related['start_date'],
                    end_date=related['end_date']
                ))
        
        return self
            
    def get_related_experiences_from_person_experiences(self, person_id=None, min_permanence_days=90):
        self.set_related_experiences_from_person_experiences(person_id=person_id, min_permanence_days=min_permanence_days)
        return self._related_from_experiences


class PersonRepository(RelatedExperiencesFromExperience):
    
    _person:Person = None
    _experiences:list[Experience] = []
    
    def __init__(self, person_id=None):
        super().__init__(person_id=person_id)
    
    
    def get_person(self, person_id=None):
        return super().get_person_by_id(person_id=person_id)
    
    def get_person_experiences(self, person_id=None):
        return super().get_person_experiences_by_person_id(person_id=person_id)
    
    def get_person_related_people_by_experiences(self, person_id=None, min_permanence_days=90):
        return super().get_related_experiences_from_person_experiences(person_id=person_id, min_permanence_days=min_permanence_days)
    
    def get_person_related_people_by_contacts(self, person_id=None, only_contacts_with_related_person=True):
        person = self.get_person(person_id=person_id)
        return FindContactsByPersonId(person.id).get_query_result(only_contacts_with_related_person)
    
    def get_person_relationships(self, person_id=None, min_permanence_days=90, only_contacts_with_related_person=True):
        person_relationship = {
            'by_experiences': [],
            'by_contacts': [],
        }
        # print('get_person_related_people_by_experiences')
        person_experiences = self.get_person_related_people_by_experiences(person_id=person_id, min_permanence_days=min_permanence_days)
        for related_from_experience in person_experiences:
            related_from_experience.__data__['person'] = related_from_experience.person.__data__
            person_relationship['by_experiences'].append(related_from_experience.__data__)
            # print2(related_from_experience.__data__)
        
        # print('get_person_related_people_by_contacts')
        person_contacts = self.get_person_related_people_by_contacts(person_id=person_id, only_contacts_with_related_person=only_contacts_with_related_person)
        for related_from_contact in person_contacts:
            person_relationship['by_contacts'].append(related_from_contact)
            # print2(related_from_contact)
        
        person = self.get_person(person_id=person_id)
        person.__data__['relationships'] = person_relationship
        return person.__data__;

def print2(data):
    # Print the param __name__ and __value__
    print(getattr(data, '__name__', '') or '')
    try:
        if isinstance(data, list):
                print(json.dumps(data, indent=2))
        else:
            print(json.dumps([data], indent=2))
    except Exception as e:
        print(data)
PERSON_ID = 1


def migrate_database():
    Migration()
    
    person_relation_ships = PersonRepository(person_id=PERSON_ID).get_person_relationships(person_id=PERSON_ID)
    
    print2(person_relation_ships)
    print('-'*64)
    print(person_relation_ships['id'], ' | ', person_relation_ships['first_name'], person_relation_ships['last_name'])
    
    for relationships_by_experience in person_relation_ships['relationships']['by_experiences']:
        print(relationships_by_experience['person']['id'], ' | ', relationships_by_experience['person']['first_name'], relationships_by_experience['person']['last_name'])
    
    for relationships_by_contacts in person_relation_ships['relationships']['by_contacts']:
        print(relationships_by_contacts['id'], ' | ', relationships_by_contacts['contact_person_name'])
    
    
    
        
        
