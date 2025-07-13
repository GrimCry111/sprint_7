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
