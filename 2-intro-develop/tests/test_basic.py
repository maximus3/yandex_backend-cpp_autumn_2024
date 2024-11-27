import pytest

# Чтобы запустить тесты наберите `make docker-test-debug`


async def test_basic(service_client):
    # Отправляем имя Developer сервису
    data = {'name': 'Developer'}
    response = await service_client.post('/v1/hello', json=data)
    # Проверяем, что бэкенд обработал запрос без ошибок
    assert response.status == 200
    # Проверяем, что бэкенд вернул Hello, Developer!
    assert response.text == 'Hello, Developer!\n'


async def test_bad_request(service_client):
    # Отправляем пустой запрос сервису
    data = {}
    response = await service_client.post('/v1/hello', json=data)
    # Проверяем, что бэкенд вернул ошибку 400
    assert response.status == 400
