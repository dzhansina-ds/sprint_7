import requests
import random 
import string
import pytest
import allure 
from generator import Generator

class TestCreatingCourier:
    
    @allure.title('Создание курьера. Проверка кода и тела ответа')
    def test_create_courier_success(self):
        
        login = Generator().generate_random_string(10)
        password = Generator().generate_random_string(10)
        first_name = Generator().generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok":True}

        logging = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        courier_id = logging.json().get('id')
        requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')


    @allure.title('Создание курьеров с одинаковыми данными. Проверка реагирования системы на ввод одинаковых данных для регистрации')
    def test_create_two_identical_couriers_error(self):
        
        login = Generator().generate_random_string(10)
        password = Generator().generate_random_string(10)
        first_name = Generator().generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        first_response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert first_response.status_code == 201

        second_response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert second_response.status_code == 409
        assert second_response.json()['message'] == "Этот логин уже используется. Попробуйте другой."

        logging = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        courier_id = logging.json().get('id')
        requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')

    @allure.title('Создание курьеров с незаполненными полями (логин, пароль). Использование параметризации')
    @pytest.mark.parametrize('skipped_data', ['login', 'password'])
    def test_create_courier_with_incomplete_data_error(self,skipped_data):

        login = Generator().generate_random_string(10)
        password = Generator().generate_random_string(10)
        first_name = Generator().generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        payload[skipped_data] = None

    
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)


        assert response.status_code == 400
        assert response.json()['message'] == "Недостаточно данных для создания учетной записи"
