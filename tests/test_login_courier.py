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
    def test_login_courier_success(self):

        login = Generator().generate_random_string(10)
        password = Generator().generate_random_string(10)
        first_name = Generator().generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        requests.post(URL.COURIER, data=payload)
        response = requests.post(URL.COURIER_LOGIN, data=payload)

        assert response.status_code == 200
        assert 'id' in response.json()

        logging = requests.post(URL.COURIER_LOGIN, data=payload)
        courier_id = logging.json().get('id')
        requests.delete(f'{URL.COURIER}/{courier_id}')

    @allure.title('Логин курьера. Ошибка при незаполнении обязательных полей. Использовании параметризации')
    @pytest.mark.parametrize('skipped_data', ['login', 'password'])
    def test_login_courier_with_incomplete_data_error(self,skipped_data):
       
        payload = {
        "login": TestData.valid_login,
        "password": TestData.valid_password
    }
        payload[skipped_data] = ''

        response = requests.post(URL.COURIER_LOGIN, data=payload)

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
        response = requests.post(URL.COURIER_LOGIN, data=payload)

        assert response.status_code == 404
        assert response.json()['message'] == TestAnswer.ACCOUNT_NOT_FOUND
