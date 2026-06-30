import requests
import allure 
import string
import random
from generator import Generator
from urls import URL

class TestDeleteCourier:

    @allure.title('Удаление курьера. Успешное удаление существующего курьера. Проверка тела ответа')
    def test_delete_courier_success(self):

        login = Generator().generate_random_string(10)
        password = Generator().generate_random_string(10)
        first_name = Generator().generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        create_courier = requests.post(URL.COURIER, data=payload)
        login_courier = requests.post(URL.COURIER_LOGIN, data=payload)
        courier_id = login_courier.json().get('id')

        response = requests.delete(f'{URL.COURIER}/{courier_id}')

        assert response.status_code == 200
        assert response.json() == {"ok":True}


    @allure.title('Удаление курьера. Отправка запроса без id. Проверка тела ответа')
    def test_delete_courier_without_id_error(self):
        params_delete = {}
        
        response = requests.delete(URL.COURIER, params=params_delete)

        assert response.status_code == 404


    @allure.title('Удаление курьера. Отправка запроса с неверным id. Проверка тела ответа')
    def test_delete_courier_wrong_id_error(self):

        response = requests.delete(f'{URL.COURIER}/0')

        assert response.status_code == 404
        assert response.json()['message'] == "Курьера с таким id нет."