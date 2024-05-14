from src.lib.database.migration.migration import migrate_database

def execute():
    return migrate_database()