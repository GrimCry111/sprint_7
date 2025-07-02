import requests
from urls import LOGIN_URL
import allure

class TestLoginCourier:

    @allure.title('Проверка авторизации клиента')
    @allure.description('Проверяем валидные даные для авторизации')
    def test_login_courier_success(self, regist_courier):
        _, courier_data = regist_courier
        login_data = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        with allure.step("Отправка запроса на авторизацию"):
            login_response = requests.post(LOGIN_URL, json=login_data)
        with allure.step("Проверка успешного статус-кода 200"):
            assert login_response.status_code == 200, f"Expected 200, got {login_response.status_code}"
        with allure.step("Проверка, что 'id' является целым числом"):
            assert "id" in login_response.json(), f"Expected 'id' in response, got {login_response.json()}"

    @allure.title('Проверка обязательных полей')
    @allure.description('Проверяем, что нельзя авторизоваться только по логину или паролю')
    def test_login_missing_required_fields(self,create_courier):
        required_fields = ["login", "password"]
        for field in required_fields:
            new_login_data = {
            "login": create_courier["login"],
            "password": create_courier["password"]
            }
            del new_login_data[field] 
            with allure.step("Отправка запроса на авторизацию"):
                response = requests.post(LOGIN_URL, json=new_login_data)
            with allure.step("Проверка статуса 400"):
                assert response.status_code in [400, 504], f"Expected 400 or 504, got {response.status_code}"
            if response.status_code == 400:
                assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title('Проверка вывода ошибки при некорректном логине или пароле')
    @allure.description('Проверяем, что будет если пользователь ввёл только логин или только пароль')
    def test_login_invalid_credentials(self,regist_courier):
        _, courier_data = regist_courier
        invalid_logins = [
            {"login": "wrong_login", "password": courier_data["password"]},
            {"login": courier_data["login"], "password": "wrong_password"}
        ]
        for login_data in invalid_logins:
            with allure.step("Отправка запроса на авторизацию"):
                response = requests.post(LOGIN_URL, json=login_data)
            with allure.step("Проверка статуса 404"):
                assert response.status_code == 404, f"Expected 404, got {response.status_code}"
            with allure.step("Проверка текста ошибки"):    
                assert response.json()["message"] == "Учетная запись не найдена", f"Unexpected response: {response.json()}"

    @allure.title('Проверка попытке входа под несуществующим пользователем')
    @allure.description('Проверяем, что вернётся сообщение, что учётной записи не существует')
    def test_login_nonexistent_user(self, create_courier):
        non_existent_data = create_courier
        with allure.step("Отправка запроса на авторизацию"):
            response = requests.post(LOGIN_URL, json=non_existent_data)
        with allure.step("Отправка статус 404"):
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        with allure.step("Отправка текста ошибки"):
            assert response.json()["message"] == "Учетная запись не найдена", f"Unexpected response: {response.json()}"

    @allure.title('Проверка, что пользователь получит id')
    @allure.description('Проверяем, что пользователю вернётся уникальный id')
    def test_login_returns_id(self, regist_courier):
        
        _, courier_data = regist_courier
        login_data = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        with allure.step("Отправка запроса на авторизацию"):
            response = requests.post(LOGIN_URL, json=login_data)
        with allure.step("Отправка статус 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        with allure.step("Отправка текста ответа"):
            assert isinstance(response.json().get("id"), int), f"Expected 'id' as integer, got {response.json()}"