from src.lib.database.migration.models.db import *
from src.lib.database.migration.models.person_model import Person
from src.lib.database.migration.models.experience_model import Experience
from src.lib.database.migration.models.contact_model import Contact


def database_connect():
    try:
        db.connect()
    except:
        print('Database connection already exists')
        db.close()
        try:
            db.connect()
        except Exception as e:
            msg = 'Database connection could not be established: {}'.format(e)
            print(msg)
            raise Exception(msg)

def database_migration_create_tables():
    try:
        db.create_tables([Person, Experience, Contact])
    except Exception as e:
        msg = 'Database migration could not be completed: {}'.format(e)
        print(msg)
        raise Exception(msg)
