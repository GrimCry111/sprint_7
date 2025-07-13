# Параметры для тестирования
TEST_CASES = [
    # Базовый запрос без параметров
    ({}, {"expected_status": 200, "check_orders": True, "check_page_info": True, "check_stations": True}),

    # Существующий courierId
    ({"courierId": 561992}, {"expected_status": 200, "check_orders": True, "check_page_info": True}),

    # Несуществующий courierId
    ({"courierId": 999999}, {"expected_status": 404, "error_message": "Курьер с идентификатором 999999 не найден"}),

    # Пагинация: первая страница, limit=1
    ({"limit": 1, "page": 0}, {"expected_status": 200, "check_orders": True, "check_page_info": True}),

    # Пагинация: вторая страница, limit=1
    ({"limit": 1, "page": 1}, {"expected_status": 200, "check_orders": True, "check_page_info": True}),

    # nearestStation с одним значением
    ({"nearestStation": '["1"]'}, {"expected_status": 200, "check_orders": True, "check_stations": True}),

    # nearestStation с несколькими значениями
    ({"nearestStation": '["1", "2"]'}, {"expected_status": 200, "check_orders": True, "check_stations": True}),
]

ORDER_COLORS = [
    ("BLACK", ["BLACK"]),
    ("GREY", ["GREY"]),
    ("BLACK+GREY", ["BLACK", "GREY"]),
    ("no color", None)
]

# Базовые данные заказа (без цвета)
BASE_ORDER_DATA = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha"
}
