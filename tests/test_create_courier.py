import requests
from urls import REGIST_URL
import allure

class TestCourier:

    @allure.title('Проверка успешного создания курьера')
    @allure.description('Проверяем, что можно создать нового курьера')
    def test_create_courier_success(self,regist_courier):
    
        response, _ = regist_courier
        
        # Проверяем статус-код
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
        
        # Проверяем тело ответа
        assert response.json() == {"ok": True}, f"Expected response {{'ok': True}}, got {response.json()}"

    @allure.title('Проверка попытки создания курьера с существующим логином')
    @allure.description('Проверяем, что нельзя создать пользователя используя уже существующий логин')
    def test_create_duplicate_courier(self,regist_courier):
        
        # Сначала создаем курьера
        response, payload = regist_courier
                
        # Пытаемся создать курьера с тем же логином
        response = requests.post(REGIST_URL, json=payload)
        
        # Проверяем статус-код
        assert response.status_code == 409, f"Expected status code 409, got {response.status_code}"
        
        # Проверяем тело ответа
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой.", f"Unexpected response: {response.json()}"

    @allure.title('Проверка, что без обязательных полей запрос выдаст ошибку')
    @allure.description('Проверяем, что нельзя создавать аккаунт без логина или пароля')
    def test_missing_required_fields(self,create_courier):
        required_fields = ["login", "password"]
        
        for field in required_fields:
            payload = create_courier
            # Удаляем одно обязательное поле
            del payload[field]
            
            response = requests.post(REGIST_URL, json=payload)
            
            # Проверяем статус-код
            assert response.status_code == 400, f"Expected status code 400 when missing {field}, got {response.status_code}"
            
            # Проверяем тело ответа
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи", f"Unexpected response when missing {field}: {response.json()}"

    #Тест невалидных данных при создании курьера
    @allure.title('Проверка невалидных данных при создании курьера')
    @allure.description('Проверяем, что нельзя создать курьера с пустыми данными')
    def test_invalid_courier_creation(self):
        
        # Пустые значения для всех полей
        payload = {
            "login": "",
            "password": "",
            "firstName": ""
        }
        response = requests.post(REGIST_URL, json=payload)
        
        # Проверяем статус-код
        assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
        
        # Проверяем тело ответа
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи", f"Unexpected response: {response.json()}"