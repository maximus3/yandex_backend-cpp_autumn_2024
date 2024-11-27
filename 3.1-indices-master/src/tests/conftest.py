import json
import os

import pytest
from httpx import AsyncClient
from tortoise import Tortoise, run_async

from enterprise.app import app
from config import TORTOISE_ORM


DATABASE_NAME = os.getenv("DATABASE_NAME", "homework")
DATABASE_USER = os.getenv("DATABASE_USER", "user")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "random")
DATABASE_HOST = os.getenv("DATABASE_HOST", "store")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

DATABASE_URL = f"postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

successful_tests = []
failed_tests = []
tests_count = 0


@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    async def init():
        await Tortoise.init(config=TORTOISE_ORM)
        # Не создаем схемы, так как база данных уже создана

    run_async(init())
    yield
    run_async(Tortoise.close_connections())


@pytest.fixture
def client():
    yield AsyncClient(app=app, base_url="http://test")


@pytest.fixture(scope="session", autouse=True)
def read_indexes(initialize_db):
    async def run_scripts():
        path = os.path.normpath(f'{os.path.dirname(os.path.abspath(__file__))}/../../tasks')
        solutions = (
            f"{path}/task_v1.sql",
            f"{path}/task_v2.sql",
            f"{path}/task_v3_orders.sql",
        )
        conn = Tortoise.get_connection("default")
        
        for file in solutions:
            try:
                with open(file) as sql:
                    if raw_sql := sql.read():
                        await conn.execute_script(raw_sql)
            except Exception as e:
                print(e)
        
        await conn.execute_query("SELECT pg_stat_reset();")

    run_async(run_scripts())
    

def pytest_runtest_logreport(report):
    if report.when == "call":
        global tests_count
        tests_count += 1
        if report.passed:
            successful_tests.append(report.nodeid)
        else:
            failed_tests.append(report.nodeid)


@pytest.fixture(scope="session", autouse=True)
def send_report(request):
    def _send_report():
        path = os.path.normpath(f'{os.path.dirname(os.path.abspath(__file__))}/../../..')
        with open(f"{path}/result.json", "w") as f:
            json.dump({"tests_ok": len(successful_tests), "tests_count": tests_count, "failed": failed_tests}, f)

    request.addfinalizer(_send_report)
