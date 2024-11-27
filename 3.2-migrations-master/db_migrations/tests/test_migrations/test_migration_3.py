import pytest

from tests.test_migrations import const
from tests.test_migrations import util


MIGRATION_3 = util.get_migrations()[:4]


@pytest.mark.parametrize('table_name', const.TABLES)
@pytest.mark.pgsql(const.DB_NAME, files=MIGRATION_3)
def test_description(assert_table_description, table_name):
    assert_table_description(table_name)


@pytest.mark.parametrize('table_name', const.TABLES)
@pytest.mark.pgsql(const.DB_NAME, files=MIGRATION_3)
def test_constraints(assert_table_constraints, table_name):
    assert_table_constraints(table_name)


@pytest.mark.parametrize('table_name', const.TABLES)
@pytest.mark.pgsql(const.DB_NAME, files=MIGRATION_3)
def test_data(assert_table_data, table_name):
    assert_table_data(table_name)


class TestCornerCases:
    ALL_MIGRATIONS = util.get_migrations()
    MIGRATION_3_WITH_EXTRA = (
        ALL_MIGRATIONS[:3] + 
        [const.EXTRA_MODIFY_SQL] + 
        ALL_MIGRATIONS[3:4]
    )

    @pytest.mark.parametrize('table_name', const.TABLES)
    @pytest.mark.pgsql(const.DB_NAME, files=MIGRATION_3_WITH_EXTRA)
    def test_data(self, assert_table_data, table_name):
        assert_table_data(table_name, with_extra=True)
