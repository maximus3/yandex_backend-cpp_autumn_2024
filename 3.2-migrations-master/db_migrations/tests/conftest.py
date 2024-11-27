import pathlib
import sys

import pytest

from testsuite.databases.pgsql import discover


pytest_plugins = [
    'testsuite.pytest_plugin',
    'testsuite.databases.pgsql.pytest_plugin',
]


@pytest.fixture(scope='session')
def project_root():
    """Path to project root."""
    return pathlib.Path(__file__).parent.parent


@pytest.fixture(scope='session')
def pgsql_local(project_root, pgsql_local_create):
    databases = discover.find_schemas(
        'db_migrations', [project_root.joinpath('schemas/postgresql')],
    )
    return pgsql_local_create(list(databases.values()))
