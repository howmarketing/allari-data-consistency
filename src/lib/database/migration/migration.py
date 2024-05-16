import json

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
    """
    The `Migration` class is responsible for managing the database migration process. It handles the following tasks:
    
    1. Connecting to the database
    2. Creating the necessary database tables
    3. Loading JSON data from files
    4. Consolidating and transforming the loaded data
    5. Creating person and contact records in the database
    
    The class has several private properties to store the loaded data, and various methods to perform the different migration tasks.
    
    The `database_connect()` method ensures the database connection is established before proceeding with the migration.
    
    The `migrate_tables()` method creates the necessary database tables (Person, Experience, Contact, Phone) if they don't already exist.
    
    The `load_json_file_data()` method is a helper function to load JSON data from a file, specified by a file key.
    
    The `load_persons_json_file_data()` and `load_contacts_json_file_data()` methods use the `load_json_file_data()` helper to load the person and contact data from their respective JSON files.
    
    The `consolidate_persons_data()` and `consolidate_contacts_data()` methods transform the loaded JSON data into a more structured format, ready for insertion into the database.
    
    The `create_person_records()` and `create_contact_records()` methods create the actual records in the database, based on the consolidated data.
    """
    
    # private property persons data
    _persons_data = []
    
    # private property contacts data
    _contacts_data = []
    
    # Constructor
    def __init__(self):
        """
        Initializes the Migration class. This method performs the following tasks:
        1. Connects to the database.
        2. Creates the necessary database tables.
        3. Loads JSON data from files.
        4. Consolidates and transforms the loaded data.
        5. Creates person and contact records in the database.

        Raises:
            Exception: If any error occurs during the database migration process.
        """
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
        """
        Returns the persons data stored in the `_persons_data` attribute.
        """
        return self._persons_data

    def get_contacts_data(self):
        """
        Returns the contacts data loaded from the JSON file.
        
        Returns:
            list: A list of contact records loaded from the JSON file.
        """
        return self._persons_data
    
    
    # Method to connect to the database
    def database_connect(self):
        """
        Attempts to connect to the database if it is not already connected.
        """
        if not is_database_connected():
            database_connect()

    def migrate_tables(self):
        """
        Attempts to create the database tables for the Person, Experience, Contact, and Phone models. If an exception occurs during the table creation, a message is printed and the exception is re-raised.
        """
        try:
            db.create_tables([Person, Experience, Contact, Phone])
        except Exception as e:
            msg = 'Database migration could not be completed: {}'.format(e)
            print(msg)
            raise Exception(msg)
    # Method to create database tables
    def create_tables():
        """
        Creates the necessary database tables for the application.
        
        Attempts to create the following tables in the database:
        - Person
        - Experience
        - Contact
        - Phone
        
        If an exception occurs during the table creation, a message is printed and the exception is re-raised.
        """
        try:
            db.create_tables([Person, Experience, Contact, Phone])
        except Exception as e:
            msg = 'Database migration could not be completed: {}'.format(e)
            print(msg)
            raise Exception(msg)
    
    # Method to load JSON data from a file
    def load_json_file_data(self, file_key):
        """
        Loads JSON data from a file specified by the `file_key` parameter.
        
        Args:
            file_key (str): The key to look up the file path in the `FILES` dictionary.
        
        Returns:
            dict: The JSON data loaded from the file.
        
        Raises:
            Exception: If the file could not be found or loaded.
        """
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
        """
        Loads person data from a JSON file and stores it in the `_persons_data` attribute.
        """
        self._persons_data = self.load_json_file_data('person_records')
    
    # Method to load contacts data from json file
    def load_contacts_json_file_data(self):
        """
        Loads the contacts data from a JSON file.
        
        This method is responsible for loading the contacts data from a JSON file located in the 'contact_records' directory. The loaded data is stored in the `_contacts_data` attribute, which can then be used for further processing or creating database records.
        """
        self._contacts_data = self.load_json_file_data('contact_records')
    
    # Method to consolidate persons data
    def consolidate_persons_data(self):
        """
        Consolidates the persons data by extracting the relevant fields and normalizing the phone numbers.
        
        This method is responsible for transforming the raw persons data into a more structured format that can be easily used to create the database records. It extracts the first name, last name, phone number, and experiences from the original persons data, and normalizes the phone number using the `normalize_phone` function.
        
        The resulting consolidated data is stored in the `_persons_data` attribute, which can then be used to create the actual database records.
        """
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
        """
        Consolidates the contacts data by extracting the relevant fields and normalizing the phone numbers.
        
        This method is responsible for transforming the raw contacts data into a more structured format that can be easily used to create the database records. It extracts the owner ID, nickname, and phone numbers from the original contacts data, and normalizes the phone numbers using the `normalize_phone` function.
        
        The resulting consolidated data is stored in the `_contacts_data` attribute, which can then be used to create the actual database records.
        """
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
        """
        Creates person records in the database based on the consolidated persons data.
        
        This method iterates through the `_persons_data` list, which contains the consolidated persons data. For each person, it creates a new `Person` entity in the database using the `Person.create()` method, passing in the consolidated person data as keyword arguments.
        
        After creating the `Person` entity, it then iterates through the `experiences` list for that person, and creates a new `Experience` entity for each experience, associating it with the newly created `Person` entity by setting the `person_id` field.
        
        This method is responsible for persisting the consolidated persons data to the database.
        """
        for person in self._persons_data:
            personEntity = Person.create(**person)
            for exp in person['experiences']:
                exp['person_id'] = personEntity.id
                Experience.create(**exp)
    
    def create_contact_records(self):
        """
        Creates contact records in the database based on the consolidated contacts data.
        
        This method iterates through the `_contacts_data` list, which contains the consolidated contacts data. For each contact, it creates a new `Contact` entity in the database using the `Contact.create()` method, passing in the consolidated contact data as keyword arguments.
        
        After creating the `Contact` entity, it then iterates through the `phones` list for that contact, and creates a new `Phone` entity for each phone number, associating it with the newly created `Contact` entity by setting the `contact_id` field.
        
        This method is responsible for persisting the consolidated contacts data to the database.
        """
        for contact in self._contacts_data:
            contactEntity = Contact.create(**contact)
            for phone in contact['phones']:
                phone['contact_id'] = contactEntity.id
                Phone.create(**phone)

