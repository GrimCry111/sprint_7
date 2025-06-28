import pytest
import requests
from urls import ORDER_URL
from data_tests import ORDER_COLORS, BASE_ORDER_DATA
import allure

class TestCreateOrder:

    @allure.title('Проверка создания заказов')
    @allure.description('Проверяем создание заказов с разными входными данными')
    @pytest.mark.parametrize("case, color", ORDER_COLORS)
    def test_create_order_with_color(self, case, color):
        
        # Формируем payload
        payload = BASE_ORDER_DATA.copy()
        if color is not None:
            payload["color"] = color

        # Отправляем запрос на создание заказа
        response = requests.post(ORDER_URL, json=payload)

        # Проверяем статус-код
        assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"

        # Проверяем наличие поля 'track'
        response_json = response.json()
        assert "track" in response_json, f"Expected 'track' in response, got {response_json}"
        assert isinstance(response_json["track"], int), f"Expected 'track' as integer, got {type(response_json['track'])}"