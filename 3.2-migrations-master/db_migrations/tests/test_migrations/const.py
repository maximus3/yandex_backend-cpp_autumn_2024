# db
DB_NAME = 'db_migrations_homework'
DB_SCHEMA = 'public'

# tables
RENT_TABLE = 'spaceship_rent'

TABLES = (
    'driver',
    'spaceship_manufacturer',
    'spaceship_model',
    'spaceship',
    RENT_TABLE,
)

# migrations
MIGRATIONS_PATH = ('migrations', )
RELATIVE_PATH_PREFIX = '../../../../migrations/'

# filenames
EXTRA_PREFIX = 'extra_'
EXTRA_MODIFY_SQL = 'extra_modify.sql'
TABLE_DESCRIPTIONS_FILENAME = 'tables.json'
TABLE_CONSTRAINTS_FILENAME = 'constraints.json'
TABLE_DATA_FILENAME = 'data.json'
