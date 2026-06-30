import requests
import allure 
import string
import random
from generator import Generator
from urls import URL
from data import TestAnswer

class TestDeleteCourier:

    @allure.title('Удаление курьера. Успешное удаление существующего курьера. Проверка тела ответа')
    def test_delete_courier_success(self,create_courier):
        payload = create_courier
        
        with allure.step('Логин курьера. Получение его id'):
            login_courier = requests.post(URL.COURIER_LOGIN, data=payload)
            courier_id = login_courier.json().get('id')

        with allure.step('Удаление курьера по id. Проверка ответа'):
            response = requests.delete(f'{URL.COURIER}/{courier_id}')
        with allure.step('Проверка ответа'):
            assert response.status_code == 200
            assert response.json() == TestAnswer.SUCCESS_TEXT


    @allure.title('Удаление курьера. Отправка запроса без id. Проверка тела ответа')
    def test_delete_courier_without_id_error(self):
        params_delete = {}
        
        with allure.step('Отправка запроса на удаление курьера без указания id. Проверка ответа'):
            response = requests.delete(URL.COURIER, params=params_delete)
        with allure.step('Проверка ответа'):
            assert response.status_code == 404


    @allure.title('Удаление курьера. Отправка запроса с неверным id. Проверка тела ответа')
    def test_delete_courier_wrong_id_error(self):

        with allure.step('Отправка запроса на удаление курьера c неверным id. Проверка ответа'):
            response = requests.delete(f'{URL.COURIER}/0')
        with allure.step('Проверка ответа'):
            assert response.status_code == 404
            assert response.json()['message'] == TestAnswer.COURIER_NOT_FOUND