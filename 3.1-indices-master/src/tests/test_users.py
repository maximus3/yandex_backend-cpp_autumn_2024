import time
from functools import wraps

import pytest


def async_timeit(duration):
    def wrapper(method):
        @wraps(method)
        async def timed(*args, **kwargs):
            ts = time.time()
            result = await method(*args, **kwargs)
            te = time.time()
            execute_time = int((te - ts) * 1000)
            assert execute_time < duration, f"Execution time {execute_time}ms exceeded {duration}ms"

            return result

        return timed

    return wrapper

def timeit(duration):
    def wrapper(method):
        @wraps(method)
        def timed(*args, **kwargs):
            ts = time.time()
            result = method(*args, **kwargs)
            te = time.time()
            execute_time = int((te - ts) * 1000)
            assert execute_time < duration, f"Execution time {execute_time}ms exceeded {duration}ms"

            return result

        return timed

    return wrapper



@async_timeit(duration=20)
async def test_async():
    assert True is True

async def test_hello(client):
    response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "search",
    ("Josh", "Иван", "Dunin", "NotFoundValue"),
)
@async_timeit(duration=250)
async def test_v1(client, search):    
    response = await client.get(f"/v1/users/?search={search}")
    assert response.status_code == 200, response.status_code


@pytest.mark.parametrize(
    "search",
    ("Josh", "Ivan", "Dunin", "NotFoundValue"),
)
@async_timeit(duration=750)
async def test_v2(client, search):
    response = await client.get(f"/v2/users/?search={search}")
    assert response.status_code == 200, response.status_code


@pytest.mark.parametrize(
    "search",
    ("Иван", "Сергеевич", "Иванова"),
)
@async_timeit(duration=750)
async def test_v2_ru(client, search):
    response = await client.get(f"/v2/users/?search={search}")
    assert response.status_code == 200, response.status_code
