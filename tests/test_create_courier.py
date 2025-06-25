import requests
import random
from faker import Faker

class TestCourier:
    # Базовый URL для тестирования
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"
    faker = Faker()
    
    #Генерация случайного payload для создания курьера
    def generate_payload(self):
        random_number = random.randint(1000, 9999)
        return {
            "login": f"{self.faker.user_name()}_{random_number}",
            "password": self.faker.password(length=6),
            "firstName": self.faker.first_name()
        }

    #Тест успешного создания курьера
    def test_create_courier_success(self):
        
        payload = self.generate_payload()
        response = requests.post(self.BASE_URL, json=payload)
        print(payload)
        
        # Проверяем статус-код
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
        
        # Проверяем тело ответа
        assert response.json() == {"ok": True}, f"Expected response {{'ok': True}}, got {response.json()}"

    #Тест попытки создания курьера с существующим логином
    def test_create_duplicate_courier(self):
        
        # Сначала создаем курьера
        payload = self.generate_payload()
        response = requests.post(self.BASE_URL, json=payload)
        print(payload)
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
        assert response.json() == {"ok": True}, f"Expected response {{'ok': True}}, got {response.json()}"
        
        # Пытаемся создать курьера с тем же логином
        response = requests.post(self.BASE_URL, json=payload)
        
        # Проверяем статус-код
        assert response.status_code == 409, f"Expected status code 409, got {response.status_code}"
        
        # Проверяем тело ответа
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой.", f"Unexpected response: {response.json()}"

    #Тест отсутствующих обязательных полей
    def test_missing_required_fields(self):
        required_fields = ["login", "password"]
        
        for field in required_fields:
            payload = {
                "login": "ninja",
                "password": "1234",
                "firstName": "saske"
            }
            # Удаляем одно обязательное поле
            del payload[field]
            
            response = requests.post(self.BASE_URL, json=payload)
            
            # Проверяем статус-код
            assert response.status_code == 400, f"Expected status code 400 when missing {field}, got {response.status_code}"
            
            # Проверяем тело ответа
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи", f"Unexpected response when missing {field}: {response.json()}"

    #Тест невалидных данных при создании курьера
    def test_invalid_courier_creation(self):
        
        # Пустые значения для всех полей
        payload = {
            "login": "",
            "password": "",
            "firstName": ""
        }
        response = requests.post(self.BASE_URL, json=payload)
        
        # Проверяем статус-код
        assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
        
        # Проверяем тело ответа
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи", f"Unexpected response: {response.json()}"