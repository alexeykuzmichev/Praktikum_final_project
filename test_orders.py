# Кузьмичев Алексей 36 когорта финальный проект
import pytest
import requests
from config import BASE_URL, ENDPOINTS
from data import ORDER_DATA


@pytest.fixture
def order_track():
    """Создаёт заказ и возвращает track. Проверяет статус 201."""
    response = requests.post(f"{BASE_URL}{ENDPOINTS['create_order']}", json=ORDER_DATA)
    assert response.status_code == 201, f"Ошибка создания заказа: {response.status_code}, {response.text}"
    track = response.json().get("track")
    assert track is not None, "В ответе нет поля 'track'"
    return track  # Возвращаем трек


def test_create_order_returns_201():
    """Шаг 1: Проверяем, что создание заказа возвращает 201"""
    response = requests.post(f"{BASE_URL}{ENDPOINTS['create_order']}", json=ORDER_DATA)
    assert response.status_code == 201


def test_get_order_by_track_returns_200_and_order_data(order_track):
    """Шаг 2: Проверяем, что по треку можно получить заказ и код 200"""
    params = {"t": order_track}
    response = requests.get(f"{BASE_URL}{ENDPOINTS['get_order_by_track']}", params=params)
    
    # Проверка 1: код ответа 200
    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

    # Проверка 2: в ответе есть данные о заказе
    json_response = response.json()
    assert "order" in json_response, "В ответе нет ключа 'order'"
    
    order = json_response["order"]
    assert "firstName" in order, "В заказе нет поля firstName"
    assert order["firstName"] == ORDER_DATA["firstName"], "Имя не совпадает"