import os
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Person, Experience, Contact

def load_persons_from_json(file_path, session):
    with open(file_path, 'r') as f:
        persons_data = json.load(f)  # Load persons data from JSON file

    for person_data in persons_data:  # Iterate over each person in the JSON data
        person = Person(
            first_name=person_data['first'],
            last_name=person_data['last'],
            phone=person_data['phone']
        )  # Create Person object
        session.add(person)  # Add Person object to session

        for experience_data in person_data['experience']:  # Iterate over each experience for the person
            start_date = datetime.strptime(experience_data['start'], '%Y-%m-%d')  # Convert start date from string to datetime
            end_date = None
            if experience_data['end']:
                end_date = datetime.strptime(experience_data['end'], '%Y-%m-%d')  # Convert end date, if it exists

            experience = Experience(
                company=experience_data['company'],
                title=experience_data['title'],
                start_date=start_date,
                end_date=end_date,
                person=person
            )  # Create Experience object
            session.add(experience)  # Add Experience object to session

    session.commit()  # Commit the session to save changes to the database

def load_contacts_from_json(file_path, session):
    with open(file_path, 'r') as f:
        contacts_data = json.load(f)  # Load contacts data from JSON file

    for contact_data in contacts_data:  # Iterate over each contact in the JSON data
        owner = session.query(Person).get(contact_data['owner_id'])  # Find the owner Person object using ID
        contact = Contact(
            contact_nickname=contact_data['contact_nickname'],
            phone_number=contact_data['phone'][0]['number'],
            owner=owner
        )  # Create Contact object
        session.add(contact)  # Add Contact object to session

    session.commit()  # Commit the session to save changes to the database

def get_connected_persons(session, person_id):
    person = session.query(Person).get(person_id)  # Retrieve Person object by ID
    if person:
        connected_persons = set()  # Use a set to avoid duplicate entries
        # Get connected persons through shared experiences
        for experience in person.experiences:
            for other_experience in session.query(Experience).filter_by(company=experience.company).all():
                if other_experience.person_id != person_id:
                    connected_persons.add(other_experience.person_id)
        # Get connected persons through shared contacts
        for contact in person.contacts:
            connected_persons.add(contact.owner_id)
        return list(connected_persons)  # Convert set to list before returning
    return []

def create_session(db_url):
    engine = create_engine(db_url)  # Create engine with database URL
    Base.metadata.create_all(engine)  # Create all tables in database based on models
    Session = sessionmaker(bind=engine)  # Create a Session class bound to the engine
    return Session()  # Instantiate and return a Session object

def main():
    # db_url = 'mysql+mysqlconnector://user:password@localhost/dbname'
    db_url = f"mysql+mysqlconnector://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}/{os.environ['MYSQL_DATABASE']}"
    session = create_session(db_url)  # Create a database session

    persons_file_path = '../migration/data/persons.json'
    contacts_file_path = '../migration/data/contacts.json'

    load_persons_from_json(persons_file_path, session)  # Load and add persons from JSON to database
    load_contacts_from_json(contacts_file_path, session)  # Load and add contacts from JSON to database

    person_id = int(input("Enter a person ID: "))  # Input person ID from user
    connected_persons = get_connected_persons(session, person_id)  # Get list of IDs of persons connected to the given person ID

    print("Connected persons:")
    for person_id in connected_persons:  # Iterate over each connected person ID
        person = session.query(Person).get(person_id)  # Retrieve Person object by ID
        if person:
            print(f"ID: {person.id}, First: {person.first_name}, Last: {person.last_name}")  # Print details of the connected person

    session.close()  # Close session

if __name__ == '__main__':
    main()
