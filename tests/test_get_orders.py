import pytest
import requests
from urls import ORDER_URL
import allure

@allure.step("Отправка GET-запроса")
def send_get_request(params=None):
    return requests.get(ORDER_URL, params=params)

@allure.step("Проверка статус-кода")
def assert_status_code(response, expected_status):
    assert response.status_code == expected_status, \
        f"Expected {expected_status}, got {response.status_code}. Response: {response.text}"

@allure.step("Проверка сообщения об ошибке")
def assert_error_message(response, error_message):
    assert response.json()["message"] == error_message, \
        f"Expected error message: {error_message}, got {response.json()['message']}"

@allure.step("Проверка наличия списка заказов")
def assert_orders_present(response_json):
    assert "orders" in response_json, "Expected 'orders' in response"
    assert isinstance(response_json["orders"], list), "'orders' should be a list"

@allure.step("Проверка наличия pageInfo")
def assert_page_info_present(response_json):
    assert "pageInfo" in response_json, "Expected 'pageInfo' in response"
    assert "page" in response_json["pageInfo"], "'pageInfo' should contain 'page'"
    assert "total" in response_json["pageInfo"], "'pageInfo' should contain 'total'"
    assert "limit" in response_json["pageInfo"], "'pageInfo' should contain 'limit'"

@allure.step("Проверка наличия availableStations")
def assert_available_stations_present(response_json):
    assert "availableStations" in response_json, "Expected 'availableStations' in response"
    assert isinstance(response_json["availableStations"], list), "'availableStations' should be a list"

@allure.step("Отправка GET-запроса")
def send_get_request(params=None):
    return requests.get(ORDER_URL, params=params)

# Основной тестовый класс
@allure.feature("Получение списка заказов")
class TestGetOrders:

    @allure.title("Получение заказов без параметров")
    @allure.description("Проверка успешного ответа с полными данными")
    def test_get_orders_without_params(self):
        params = {}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_page_info": True,
            "check_stations": True
        }

        response = send_get_request(params)
        assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        if expected["expected_status"] == 200:
            assert_orders_present(response_json)
            assert_page_info_present(response_json)
            assert_available_stations_present(response_json)

    @allure.title("Получение заказов с существующим courierId")
    @allure.description("Проверка успешного ответа с данными курьера")
    def test_get_orders_with_existing_courier(self):
        params = {"courierId": 561992}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_page_info": True
        }

        response = send_get_request(params)
        assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        if expected["expected_status"] == 200:
            assert_orders_present(response_json)
            assert_page_info_present(response_json)

    @allure.title("Получение заказов с несуществующим courierId")
    @allure.description("Проверка ошибки 404 и сообщения об отсутствии курьера")
    def test_get_orders_with_nonexistent_courier(self):
        params = {"courierId": 999999}
        expected = {
            "expected_status": 404,
            "error_message": "Курьер с идентификатором 999999 не найден"
        }

        response = send_get_request(params)
        assert_status_code(response, expected["expected_status"])
        assert_error_message(response, expected["error_message"])

    @allure.title("Получение заказов: первая страница пагинации")
    @allure.description("Проверка успешного ответа с пагинацией (page=0, limit=1)")
    def test_pagination_first_page(self):
        params = {"limit": 1, "page": 0}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_page_info": True
        }

        response = send_get_request(params)
        assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        if expected["expected_status"] == 200:
            assert_orders_present(response_json)
            assert_page_info_present(response_json)

    @allure.title("Получение заказов: вторая страница пагинации")
    @allure.description("Проверка успешного ответа с пагинацией (page=1, limit=1)")
    def test_pagination_second_page(self):
        params = {"limit": 1, "page": 1}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_page_info": True
        }

        response = send_get_request(params)
        assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        if expected["expected_status"] == 200:
            assert_orders_present(response_json)
            assert_page_info_present(response_json)

    @allure.title("Получение заказов с nearestStation (одна станция)")
    @allure.description("Проверка успешного ответа и доступных станций")
    def test_nearest_station_single(self):
        params = {"nearestStation": '["1"]'}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_stations": True
        }

        response = send_get_request(params)
        assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        if expected["expected_status"] == 200:
            assert_orders_present(response_json)
            assert_available_stations_present(response_json)

    @allure.title("Получение заказов с nearestStation (несколько станций)")
    @allure.description("Проверка успешного ответа и доступных станций")
    def test_nearest_station_multiple(self):
        params = {"nearestStation": '["1", "2"]'}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_stations": True
        }

        response = send_get_request(params)
        assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        if expected["expected_status"] == 200:
            assert_orders_present(response_json)
            assert_available_stations_present(response_json)