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

def find_connections_via_contacts(person_records, person_id, contact_records):
    person = next((p for p in person_records if p['id'] == person_id), None)
    if not person:
        return []

    person_contacts = chain.from_iterable(
        [c['phone'] for c in contact_records if c['owner_id'] == person_id]
    )
    # person_contacts = [normalize_phone(c) for c in person_contacts]
    person_contacts = [normalize_phone(c['number']) for c in person_contacts]

    
    connected_persons = []
    for other_person in person_records:
        if other_person['id'] == person_id:
            continue

        other_contacts = chain.from_iterable(
            [c['phone'] for c in contact_records if c['owner_id'] == other_person['id']]
        )
        other_contacts = [normalize_phone(c['number']) for c in other_contacts]

        if any(c in other_contacts for c in person_contacts):
            connected_persons.append(other_person['id'])

    connected_persons.append(person_id)
    return connected_persons

def find_connections_via_experiences(person_records, person_id):
    person = next((p for p in person_records if p['id'] == person_id), None)
    if not person:
        return []

    person_companies = [exp['company'] for exp in person.get('experience', [])]
    connected_persons = [person_id]

    for other_person in person_records:
        if other_person['id'] == person_id:
            continue

        other_companies = [exp['company'] for exp in other_person.get('experience', [])]
        overlapping_companies = set(person_companies) & set(other_companies)

        if overlapping_companies:
            for company in overlapping_companies:
                person_exp = next((exp for exp in person['experience'] if exp['company'] == company), None)
                other_exp = next((exp for exp in other_person['experience'] if exp['company'] == company), None)

                if person_exp and other_exp:
                    person_start = normalize_date(person_exp['start'])
                    person_end = normalize_date(person_exp['end']) if person_exp['end'] else datetime.now()
                    other_start = normalize_date(other_exp['start'])
                    other_end = normalize_date(other_exp['end']) if other_exp['end'] else datetime.now()

                    overlap = (min(person_end, other_end) - max(person_start, other_start)).total_seconds() / 86400
                    if overlap >= 90:
                        connected_persons.append(other_person['id'])
                        break

    return connected_persons


def main(person_records, person_id, contact_records):
    connections_via_contacts = find_connections_via_contacts(person_records, person_id, contact_records)
    connections_via_experiences = find_connections_via_experiences(person_records, person_id)

    all_connections = sorted(set(connections_via_contacts + connections_via_experiences))

    print("Connected persons:")
    for conn_id in all_connections:
        person = next((p for p in person_records if p['id'] == conn_id), None)
        if person:
            print(f"ID: {conn_id} - First/Last: {person['first']} {person['last']}")

if __name__ == "__main__":
    import sys
    person_id = int(sys.argv[1])
    person_records = load_person_records('src/lib/migration/data/persons.json')
    contact_records = load_contacts('src/lib/migration/data/contacts.json')
    main(person_records, person_id, contact_records)
