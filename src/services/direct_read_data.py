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


def normalize_phone(phone):
    if not phone:
        return None
    return phone.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')

def normalize_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, "%Y-%m-%d")