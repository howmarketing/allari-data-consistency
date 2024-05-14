import json
# Import necessary modules and models

from src.lib.database.conn import db, database_connect
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

# Initialize empty lists to store records
RECORDS={
    'person_records':   [],
    'contact_records':  [],
}

def migrate_database():
    
    # Function to check if the database is connected
    def is_database_connected():
        return False if db.is_closed() else True

    # Function to create database tables
    def database_migration_create_tables():
        try:
            db.create_tables([Person, Experience, Contact, Phone])
        except Exception as e:
            msg = 'Database migration could not be completed: {}'.format(e)
            print(msg)
            raise Exception(msg)
    
    # Function to load JSON data from a file
    def load_json_data(file_key) -> list[any]:
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
    
    
    
    # Function to load person records from JSON data
    def load_person_records() -> dict[str, any]:
        # Defining constants
        file_key:str = 'person_records'
        items:list[any] = []
        response = {
            'success': False,
            'msg': 'not executed',
            'data': []
        }
        
        # Execution block
        try:
            
            # Load the items
            try:
                items = load_json_data(file_key)
            except Exception as e:
                msg = '(File could not be loaded): {}'.format(e)
                print(msg)
                raise Exception(msg)
            
            # Iterate over the items recording each item Block
            try:
                
                # Iterate over each item
                for item in items:
                                        
                    # Consolidating data
                    try:
                        data = {
                            'first_name': item['first'],
                            'last_name': item['last'],
                            'phone': normalize_phone(item['phone'])
                        }
                    except Exception as e:
                        msg = '(Consolidating data error): {}'.format(e)
                        print(msg)
                        raise Exception(msg)
                    
                    # Create the entity by recording the data
                    try:
                        entity:Person = Person.create(**data)
                    except Exception as e:
                        msg = '(Create entity error): {}'.format(e)
                        print(msg)
                        raise Exception(msg)
                    
                    # Define the entity experiences property as empty list
                    try:
                        entity.experiences:list[Experience] = []
                    except Exception as e:
                        msg = '(Experiences property definition as list): {}'.format(e)
                        print(msg)
                        raise Exception(msg)
                    
                    # Iterate over the experiences recording the experience and append them to the entity experiences property
                    try:
                        for exp in item['experience']:
                            # Define the experience data with the relationship between the experience and the person
                            exp_data = {
                                'title'        :    exp['title'],
                                'company'      :    exp['company'],
                                'start_date'   :    exp['start'],
                                'end_date'     :    exp['end'],
                                'person_id'    :    entity.id                                
                            }
                            # Record the experience
                            exp_entity:Experience = Experience.create(**exp_data)
                            # Append the experience to the entity experiences property
                            entity.experiences.append(exp_entity)
                    except Exception as e:
                        msg = '(Create experience entity error): {}'.format(e)
                        print(msg)
                        raise Exception(msg)
                    
                    # Append the entity to the response data
                    try:
                        response['data'].append(entity)
                    except Exception as e:
                        msg = '(Append entity to response data error): {}'.format(e)
                        print(msg)
                        raise Exception(msg)
                
                try:
                    response['success'] = True
                    response['msg'] = 'The ({}) records were successfully recorded'.format(len(response['data']))
                except Exception as e:
                    msg = '(Response data definition error): {}'.format(e)
                    print(msg)
                    raise Exception(msg)
            
                 # End for
            
            # End iterate block
            except Exception as e:
                msg = '(Iterate items error): {}'.format(e)     
                print(msg)
                raise Exception(msg)
        
        # End the block execution
        except Exception as e:
            msg = '[ERROR] load_person_records{}'.format(e)
            response['success'] = False
            response['msg'] = msg
            print(msg)
            raise Exception(msg)
        
        return response       
    
    # Function to load contact records from JSON data
    def load_contact_records() -> dict[str, any]:
        # Defining constants
        file_key:str = 'contact_records'
        items:list[any] = []
        response = {
            'success': False,
            'msg': 'not executed',
            'data': []
        }
        
        # Execution block
        try:
            
            # Load the items
            try:
                items = load_json_data(file_key)
            except Exception as e:
                msg = '(File could not be loaded): {}'.format(e)
                print(msg)
                raise Exception(msg)
            
            # Iterate over the items recording each item Block
            try:
                
                # Iterate over each item
                for item in items:
                                        
                    # Consolidating data
                    try:
                        data = {
                            'owner_id': item['owner_id'],
                            'nickname': item['contact_nickname']
                        }
                    except Exception as e:
                        msg = '(Consolidating data error): {}'.format(e)
                        print(msg)
                        raise Exception(msg)
                    
                    
                    # Create the entity by recording the data
                    try:
                        entity:Person = Contact.create(**data)
                    except Exception as e:
                        msg = '(Create entity error): {}'.format(e)
                        print(msg)
                        raise Exception(msg)
                    
                    # Define the entity phones property as empty list
                    try:
                        entity.phones:list[Phone] = []
                    except Exception as e:
                        msg = '(Phones property definition as list): {}'.format(e)
                        print(msg)
                        raise Exception(msg)
                    
                    # Iterate over the phones recording the phone and append them to the entity phones property
                    try:
                        for phone in item['phone']:
                            # Define the experience data with the relationship between the experience and the person
                            phone_data = {
                                'type'          :     phone['type'],
                                'number'        :     phone['number'],
                                'contact_id'    :     entity.id
                            }
                            # Record the experience
                            phone_entity:Phone = Phone.create(**phone_data)
                            # Append the phone to the entity phones property
                            entity.phones.append(phone_entity)
                    except Exception as e:
                        msg = '(Create phone entity error): {}'.format(e)
                        print(msg)
                        raise Exception(msg)
                    
                    # Append the entity to the response data
                    try:
                        response['data'].append(entity)
                    except Exception as e:
                        msg = '(Append entity to response data error): {}'.format(e)
                        print(msg)
                        raise Exception(msg)
                
                try:
                    response['success'] = True
                    response['msg'] = 'The ({}) records were successfully recorded'.format(len(response['data']))
                except Exception as e:
                    msg = '(Response data definition error): {}'.format(e)
                    print(msg)
                    raise Exception(msg)
            
                 # End for
            
            # End iterate block
            except Exception as e:
                msg = '(Iterate items error): {}'.format(e)     
                print(msg)
                raise Exception(msg)
        
        # End the block execution
        except Exception as e:
            msg = '[ERROR] load_contact_records{}'.format(e)
            response['success'] = False
            response['msg'] = msg
            print(msg)
            raise Exception(msg)
        
        return response       
    

    try:
        # Connect to the database if not connected
        if not is_database_connected():
            database_connect()
        
        # Create database tables
        database_migration_create_tables()
        print('Database migration create tables completed')
        
        # Load person records
        load_persons_response = load_person_records()
        print('{}'.format(load_persons_response['msg']))        
        
        # Load contact records
        load_contacts_response = load_contact_records()
        print('{}'.format(load_contacts_response['msg']))
        
        
    except Exception as e:
        msg = 'Database migration could not be completed: {}'.format(e)
        print(msg)
        raise Exception(msg)
