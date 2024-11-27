import pytest

from testsuite.databases import pgsql

# Start the tests via `make test-debug` or `make test-release`


@pytest.mark.pgsql('db-1', files=['initial_data.sql'])
async def test_wrong_user_id(service_client):
    user_id = '12123123'
    item_ids = ['cOmmOn_26']

    response = await service_client.get(
        '/check',
        params={
            'user_id': user_id,
            'item_id': item_ids
        },
    )
    response_json = response.json()

    assert response.status == 200
    assert len(response_json) == len(item_ids)
    assert response_json[0]["problem"] == "NO_USER"
    assert response_json[0]["item_id"] == item_ids[0]


def find_problem(response_json, item_id):
    return next((item["problem"] for item in response_json if item["item_id"] == item_id), None)


@pytest.mark.pgsql('db-1', files=['initial_data.sql'])
async def test_default_user_without_receipt_all_categories(service_client):
    user_id = '1'
    item_ids = ['common_1', 'special_1', 'receipt_1', 'cringe_228']

    response = await service_client.get(
        '/check',
        params={
            'user_id': user_id,
            'item_id': item_ids
        },
    )
    response_json = response.json()

    assert response.status == 200
    assert len(response_json) == 3
    assert find_problem(response_json, 'special_1') == "ITEM_IS_SPECIAL"
    assert find_problem(response_json, 'receipt_1') == "NO_RECEIPT"
    assert find_problem(response_json, 'cringe_228') == "WRONG_DATA"


@pytest.mark.pgsql('db-1', files=['initial_data.sql'])
async def test_default_user_with_receipt(service_client):
    user_id = '3'
    item_ids = ['receipt_10', 'receipt_42', 'receipt_68', 'receipt_1337228']

    response = await service_client.get(
        '/check',
        params={
            'user_id': user_id,
            'item_id': item_ids
        },
    )
    response_json = response.json()

    assert response.status == 200
    assert len(response_json) == 2
    assert find_problem(response_json, 'receipt_68') == "NO_RECEIPT"
    assert find_problem(response_json, 'receipt_1337228') == "ITEM_NOT_FOUND"


@pytest.mark.pgsql('db-1', files=['initial_data.sql'])
async def test_doctor(service_client):
    user_id = '61'
    item_ids = ['common_1', 'receipt_1', 'special_16', 'special_17']

    response = await service_client.get(
        '/check',
        params={
            'user_id': user_id,
            'item_id': item_ids
        },
    )
    response_json = response.json()
    assert response.status == 200
    assert len(response_json) == 1
    assert find_problem(
        response_json, 'special_17') == "ITEM_SPECIAL_WRONG_SPECIFIC"


@pytest.mark.pgsql('db-1', files=['initial_data.sql'])
async def test_all_good(service_client):
    user_id = 61
    item_ids = ['common_1', 'receipt_1', 'special_16']

    response = await service_client.get(
        '/check',
        params={
            'user_id': user_id,
            'item_id': item_ids
        },
    )
    response_json = response.json()

    assert response.status == 200
    assert len(response_json) == 0


@pytest.mark.pgsql('db-1', files=['initial_data.sql'])
async def test_empty_request(service_client):
    user_id = 1
    item_ids = []

    response = await service_client.get(
        '/check',
        params={
            'user_id': user_id,
            'item_id': item_ids
        },
    )
    response_json = response.json()

    assert response.status == 200
    assert len(response_json) == 0
