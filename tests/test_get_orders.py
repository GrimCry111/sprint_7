import allure
import helper

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

        response = helper.send_get_request(params)
        helper.assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        helper.assert_orders_present(response_json)
        helper.assert_page_info_present(response_json)
        helper.assert_available_stations_present(response_json)

    @allure.title("Получение заказов с существующим courierId")
    @allure.description("Проверка успешного ответа с данными курьера")
    def test_get_orders_with_existing_courier(self):
        params = {"courierId": 561992}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_page_info": True
        }

        response = helper.send_get_request(params)
        helper.assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        helper.assert_orders_present(response_json)
        helper.assert_page_info_present(response_json)

    @allure.title("Получение заказов с несуществующим courierId")
    @allure.description("Проверка ошибки 404 и сообщения об отсутствии курьера")
    def test_get_orders_with_nonexistent_courier(self):
        params = {"courierId": 999999}
        expected = {
            "expected_status": 404,
            "error_message": "Курьер с идентификатором 999999 не найден"
        }

        response = helper.send_get_request(params)
        helper.assert_status_code(response, expected["expected_status"])
        helper.assert_error_message(response, expected["error_message"])

    @allure.title("Получение заказов: первая страница пагинации")
    @allure.description("Проверка успешного ответа с пагинацией (page=0, limit=1)")
    def test_pagination_first_page(self):
        params = {"limit": 1, "page": 0}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_page_info": True
        }

        response = helper.send_get_request(params)
        helper.assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        helper.assert_orders_present(response_json)
        helper.assert_page_info_present(response_json)

    @allure.title("Получение заказов: вторая страница пагинации")
    @allure.description("Проверка успешного ответа с пагинацией (page=1, limit=1)")
    def test_pagination_second_page(self):
        params = {"limit": 1, "page": 1}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_page_info": True
        }

        response = helper.send_get_request(params)
        helper.assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        helper.assert_orders_present(response_json)
        helper.assert_page_info_present(response_json)

    @allure.title("Получение заказов с nearestStation (одна станция)")
    @allure.description("Проверка успешного ответа и доступных станций")
    def test_nearest_station_single(self):
        params = {"nearestStation": '["1"]'}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_stations": True
        }

        response = helper.send_get_request(params)
        helper.assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        helper.assert_orders_present(response_json)
        helper.assert_available_stations_present(response_json)

    @allure.title("Получение заказов с nearestStation (несколько станций)")
    @allure.description("Проверка успешного ответа и доступных станций")
    def test_nearest_station_multiple(self):
        params = {"nearestStation": '["1", "2"]'}
        expected = {
            "expected_status": 200,
            "check_orders": True,
            "check_stations": True
        }

        response = helper.send_get_request(params)
        helper.assert_status_code(response, expected["expected_status"])
        response_json = response.json()

        helper.assert_orders_present(response_json)
        helper.assert_available_stations_present(response_json)