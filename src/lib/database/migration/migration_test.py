import json
from src.lib.database.conn import db, database_connect
from src.lib.database.migration.models.person_model import Person
from src.lib.database.migration.models.experience_model import Experience
from src.lib.database.migration.models.contact_model import Contact
from src.lib.database.migration.models.phone_model import Phone
from src.lib.helpers.format import normalize_phone
from src.lib.database.migration.migration import migrate_database

def execute():
    return migrate_database()