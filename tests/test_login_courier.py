import requests
from data import TestData, TestAnswer
import pytest
import allure 
import string
import random
from generator import Generator
from urls import URL

class TestLoginCourier:

    @allure.title('Логин курьера. Успешная авторизация с валидными данными. Проверка тела ответа')
    def test_login_courier_success(self,create_courier):
        payload = create_courier
        with allure.step('Запрос на авторизацию курьера'):
            response = requests.post(URL.COURIER_LOGIN, data=payload)
        with allure.step('Проверка ответа'):
            assert response.status_code == 200
            assert 'id' in response.json()


    @allure.title('Логин курьера. Ошибка при незаполнении обязательных полей. Использовании параметризации')
    @pytest.mark.parametrize('skipped_data', ['login', 'password'])
    def test_login_courier_with_incomplete_data_error(self,skipped_data):
       
        payload = {
        "login": TestData.valid_login,
        "password": TestData.valid_password
    }
        payload[skipped_data] = ''
        with allure.step('Отправка запроса на авторизацию курьера с незаполнеными обязательными полями'):
            response = requests.post(URL.COURIER_LOGIN, data=payload)
        with allure.step('Проверка ответа'):
            assert response.status_code == 400
            assert response.json()['message'] == TestAnswer.INCOMPLETE_DATA_FOR_ENTER

    @allure.title('Логин курьера. Ошибка при использовании невалидных данных')
    @pytest.mark.parametrize(
        'login,password',
        [
            [TestData.invalid_login, TestData.valid_password],
            [TestData.valid_login, TestData.invalid_password],
            [TestData.invalid_login, TestData.invalid_password]
        ]
    )
    def test_login_courier_with_invalid_data_error(self,login,password):
        
        payload = {
        "login": login,
        "password": password
    }
        with allure.step('Отправка запроса на авторизацию курьера с невалидными данными'):
            response = requests.post(URL.COURIER_LOGIN, data=payload)
        with allure.step('Проверка ответа'):
            assert response.status_code == 404
            assert response.json()['message'] == TestAnswer.ACCOUNT_NOT_FOUND
