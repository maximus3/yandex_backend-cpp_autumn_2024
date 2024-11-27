import pytest

from tests.test_migrations import const
from tests.test_migrations import util


MIGRATION_2 = util.get_migrations()[:3]


@pytest.mark.parametrize('table_name', const.TABLES)
@pytest.mark.pgsql(const.DB_NAME, files=MIGRATION_2)
def test_data(assert_table_data, table_name):
    assert_table_data(table_name)
