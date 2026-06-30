import requests
from data import TestData
import pytest
import allure 
import string
import random
from generator import Generator

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

        requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)

        assert response.status_code == 200
        assert 'id' in response.json()

        logging = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        courier_id = logging.json().get('id')
        requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')

    @allure.title('Логин курьера. Ошибка при незаполнении обязательных полей. Использовании параметризации')
    @pytest.mark.parametrize('skipped_data', ['login', 'password'])
    def test_login_courier_with_incomplete_data_error(self,skipped_data):
       
        payload = {
        "login": TestData.valid_login,
        "password": TestData.valid_password
    }
        payload[skipped_data] = ''

        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)

        assert response.status_code == 400
        assert response.json()['message'] == "Недостаточно данных для входа"

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
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)

        assert response.status_code == 404
        assert response.json()['message'] == "Учетная запись не найдена"
