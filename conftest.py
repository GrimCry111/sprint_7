import pytest
import random
import requests
from urls import REGIST_URL
from faker import Faker
import allure


@pytest.fixture
@allure.step("Создадим новые учётные данные")
def create_courier():
    faker = Faker()
    random_number = random.randint(1000, 9999)
    return {
        "login": f"{faker.user_name()}_{random_number}",
        "password": faker.password(length=6),
        "firstName": faker.first_name(),
    }


@pytest.fixture
@allure.step("Зарегестрируем пользователя")
def regist_courier(create_courier):
    # Отправляем запрос на регистрацию
    response = requests.post(REGIST_URL, json=create_courier)
    # Возвращаем кортеж: (ответ, данные курьера)
    return response, create_courier


@pytest.fixture
@allure.step("Получим данные для авторизации")
def login_data(create_courier):
    return {"login": create_courier["login"], "password": create_courier["password"]}