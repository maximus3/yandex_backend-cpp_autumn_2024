import time
from functools import wraps


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


@async_timeit(duration=150)
async def test_pending_orders(client):
    response = await client.get("/pending_orders")
    assert response.status_code == 200, response.status_code
