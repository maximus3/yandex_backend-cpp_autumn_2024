import datetime

import pytest

from testsuite.utils import ordered_object

from tests.test_migrations import const
from tests.test_migrations import util


@pytest.fixture(name='fetch_table_description')
def _fetch_table_description(pgsql):
    def wrapper(table_name: str, table_schema: str = const.DB_SCHEMA):
        with pgsql[const.DB_NAME].dict_cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    column_name,
                    column_default,
                    is_nullable,
                    udt_name,
                    data_type,
                    character_maximum_length,
                    numeric_precision,
                    datetime_precision
                FROM INFORMATION_SCHEMA.COLUMNS
                where table_schema = %s AND table_name = %s;
                """,
                (table_schema, table_name),
            )

            return [dict(r) for r in cursor.fetchall()]

    return wrapper


@pytest.fixture(name='fetch_table_constraints')
def _fetch_table_constraints(pgsql):
    def wrapper(table_name: str, table_schema: str = const.DB_SCHEMA):
        with pgsql[const.DB_NAME].dict_cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    tc.constraint_type,
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_or_primary_table_name,
                    ccu.column_name AS foreign_or_primary_column_name,
                    cc.check_clause
                FROM
                    information_schema.table_constraints AS tc
                    LEFT JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                    LEFT JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                    LEFT JOIN information_schema.check_constraints AS cc
                    ON tc.constraint_name = cc.constraint_name
                    AND tc.table_schema = cc.constraint_schema
                WHERE tc.table_schema = %s AND tc.table_name = %s;
                """,
                (table_schema, table_name),
            )

            return [dict(r) for r in cursor.fetchall()]

    return wrapper


def _serialize(value):
    if isinstance(value, datetime.datetime):
        return datetime.datetime.strftime(value, '%Y-%m-%d %H:%M:%S')
    return value


def _serialize_dict(dict_):
    for key in dict_:
        value = dict_[key]
        dict_[key] = _serialize(value)
    return dict_


@pytest.fixture(name='fetch_table_data')
def _fetch_table_data(pgsql):
    def wrapper(
            table_name: str,
            order_by_column: str = 'id',
            table_schema: str = const.DB_SCHEMA,
    ):
        with pgsql[const.DB_NAME].dict_cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                    *
                FROM {table_schema}.{table_name}
                ORDER BY {order_by_column};
                """,
            )

            return [_serialize_dict(dict(r)) for r in cursor.fetchall()]

    return wrapper


@pytest.fixture(name='assert_table_description')
def _assert_table_description(fetch_table_description, load_json):
    def wrapper(
            table_name: str, table_schema: str = const.DB_SCHEMA,
    ):
        values = fetch_table_description(table_name)

        expected_data = load_json(util.table_descriptions_filename())
        expected_values = expected_data.get(table_name)

        ordered_object.assert_eq(values, expected_values, paths=[''])

    return wrapper


@pytest.fixture(name='assert_table_constraints')
def _assert_table_constraints(fetch_table_constraints, load_json):
    def wrapper(
        table_name: str, table_schema: str = const.DB_SCHEMA,
    ):
        values = fetch_table_constraints(table_name)

        expected_data = load_json(util.table_constraints_filename())
        expected_values = expected_data.get(table_name)

        ordered_object.assert_eq(values, expected_values, paths=[''])

    return wrapper


def _get_order_by_column(table_name):
    return 'driver_id' if table_name == const.RENT_TABLE else 'id'


@pytest.fixture(name='assert_table_data')
def _assert_table_data(fetch_table_data, load_json):
    def wrapper(
            table_name: str,
            with_extra: bool = False,
            table_schema: str = const.DB_SCHEMA,
    ):
        order_by_column = _get_order_by_column(table_name)
        values = fetch_table_data(table_name, order_by_column, table_schema)

        expected_data = load_json(util.table_data_filename(with_extra))
        expected_values = expected_data.get(table_name)

        ordered_object.assert_eq(values, expected_values, paths=[''])

    return wrapper
