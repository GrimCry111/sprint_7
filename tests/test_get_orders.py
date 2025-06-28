import pytest
import requests
from data_tests import TEST_CASES
from urls import ORDER_URL
import allure

class TestGetOrders:

    @allure.title('Проверка, что пользователь видит список заказов')
    @allure.description('Проверяем, что вернётся список с определёнными значениями')
    @pytest.mark.parametrize("params, expected", TEST_CASES)
    def test_get_orders(self, params, expected):
        
        # Отправляем GET-запрос
        response = requests.get(ORDER_URL, params=params)

        # Проверяем статус-код
        assert response.status_code == expected["expected_status"], \
            f"Expected {expected['expected_status']}, got {response.status_code}. Response: {response.text}"

        # Если ожидаем ошибку 404, проверяем сообщение
        if expected["expected_status"] == 404:
            assert response.json()["message"] == expected["error_message"], \
                f"Expected error message: {expected['error_message']}, got {response.json()['message']}"
            return

        # Если ожидаем успешный ответ, проверяем структуру
        response_json = response.json()

        # Проверяем наличие списка заказов
        if expected.get("check_orders"):
            assert "orders" in response_json, "Expected 'orders' in response"
            assert isinstance(response_json["orders"], list), "'orders' should be a list"

        # Проверяем pageInfo
        if expected.get("check_page_info"):
            assert "pageInfo" in response_json, "Expected 'pageInfo' in response"
            assert "page" in response_json["pageInfo"], "'pageInfo' should contain 'page'"
            assert "total" in response_json["pageInfo"], "'pageInfo' should contain 'total'"
            assert "limit" in response_json["pageInfo"], "'pageInfo' should contain 'limit'"

        # Проверяем availableStations (если есть в ответе)
        if expected.get("check_stations"):
            assert "availableStations" in response_json, "Expected 'availableStations' in response"
            assert isinstance(response_json["availableStations"], list), "'availableStations' should be a list"