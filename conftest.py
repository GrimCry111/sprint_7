import pytest
import random
import requests
from tests.urls import REGIST_URL
from faker import Faker
import allure

@allure.step('Зарегестрируем пользователя')
@pytest.fixture
def regist_courier(create_courier):
    # Отправляем запрос на регистрацию
    response = requests.post(REGIST_URL, json=create_courier)
    # Возвращаем кортеж: (ответ, данные курьера)
    return response, create_courier

@allure.step('Создадим новые учётные данные')
@pytest.fixture
def create_courier():
    faker = Faker()
    random_number = random.randint(1000, 9999)
    return {
            "login": f"{faker.user_name()}_{random_number}",
            "password": faker.password(length=6),
            "firstName": faker.first_name()
        }

@allure.step('Получим данные для авторизации')
@pytest.fixture
def login_data(create_courier):
    return {
        "login": create_courier["login"],
        "password": create_courier["password"]
    }