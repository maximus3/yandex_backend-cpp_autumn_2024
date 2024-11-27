import pathlib


from tests.test_migrations import const


def get_migrations():
    root = pathlib.Path(__file__).parent.parent.parent.parent
    folder = root.joinpath(*const.MIGRATIONS_PATH)
    files = list(
        f'{const.RELATIVE_PATH_PREFIX}{path.stem}.sql' 
        for path in folder.glob('*.sql')
    )
    return sorted(files)


def table_descriptions_filename():
    return const.TABLE_DESCRIPTIONS_FILENAME


def table_constraints_filename():
    return const.TABLE_CONSTRAINTS_FILENAME


def table_data_filename(with_extra):
    return (
        const.TABLE_DATA_FILENAME 
        if not with_extra 
        else const.EXTRA_PREFIX + const.TABLE_DATA_FILENAME
    )
