from src.lib.database.migration.models.db import db


def database_connect():
    try:
        db.connect()
    except:
        print('Database connection already exists')
        db.close()
        try:
            db.connection()
        except Exception as e:
            msg = 'Database connection could not be established: {}'.format(e)
            print(msg)
            raise Exception(msg)


def is_database_connected():
    return False if db.is_closed() else True