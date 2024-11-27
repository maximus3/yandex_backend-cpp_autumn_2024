import pytest

from tests.test_migrations import const
from tests.test_migrations import util


MIGRATION_1 = util.get_migrations()[:2]


@pytest.mark.parametrize('table_name', const.TABLES)
@pytest.mark.pgsql(const.DB_NAME, files=MIGRATION_1)
def test_description(assert_table_description, table_name):
    assert_table_description(table_name)


@pytest.mark.parametrize('table_name', const.TABLES)
@pytest.mark.pgsql(const.DB_NAME, files=MIGRATION_1)
def test_constraints(assert_table_constraints, table_name):
    assert_table_constraints(table_name)
