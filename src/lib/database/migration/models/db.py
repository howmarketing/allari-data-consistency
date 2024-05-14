from peewee import SqliteDatabase
from random import randint

database_path = 'src/lib/database/migration/data/db/'
database_name = 'allari-data-consistency_{}_.db'.format(randint(1000000, 9999999))
database = '{}{}'.format(database_path, database_name)
db = SqliteDatabase(database, pragmas={'foreign_keys': 1})
