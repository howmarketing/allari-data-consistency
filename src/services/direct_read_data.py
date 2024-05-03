import json
from datetime import datetime, timedelta
from itertools import chain

def load_contacts(contacts_file):
    with open(contacts_file, 'r') as f:
        contacts = json.load(f)
    return contacts

def load_person_records(person_file):
    with open(person_file, 'r') as f:
        person_records = json.load(f)
    return person_records

