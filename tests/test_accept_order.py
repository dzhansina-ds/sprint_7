import requests
from data import TestData, TestAnswer
import allure 
import string
import random
from generator import Generator
from urls import URL

class TestAcceptOrder:
    @allure.title('Принятие заказа. Успешный запрос с id курьера и заказа. Проверка тела ответа')
    def test_accept_order_success(self,create_courier):
        payload_courier = create_courier
        
        with allure.step('Логин курьера. Получение id курьера'):
            login_courier = requests.post(URL.COURIER_LOGIN, data=payload_courier)
            courier_id = login_courier.json().get('id')

        payload_order = {
        "firstName": TestData.firstName,
        "lastName": TestData.lastName,
        "address": TestData.address,
        "metroStation": TestData.metroStation,
        "phone": TestData.phone,
        "rentTime": TestData.rentTime,
        "deliveryDate": TestData.deliveryDate,
        "comment": TestData.comment,
        "color": []
        }
        with allure.step('Отправка запроса на создание заказа'):
            make_order = requests.post(URL.ORDERS, json=payload_order)
        with allure.step('Получение трэк-номера'):
            track_number = make_order.json().get("track")
        order_data={"t": track_number}
        with allure.step('Отправка запроса на получение информации о заказе. Получение id заказа'):
            get_order_info = requests.get(URL.ORDERS_TRACK, params=order_data)
            order_id = get_order_info.json().get('order').get('id')

        params = {
            "courierId": courier_id
        }

        with allure.step('Отправка запроса на принятие заказа'):
            response = requests.put(f'{URL.ORDERS_ACCEPT}/{order_id}', params=params)
        
        with allure.step('Проверка ответа'):
            assert response.status_code == 200
            assert response.json() == TestAnswer.SUCCESS_TEXT

    @allure.title('Принятие заказа. В запросе не указываем id курьера. Проверка тела ответа')
    def test_accept_order_without_courier_id_error(self):
        params = {}
        with allure.step('Отправка запроса на принятие заказа без указания id курьера'):
            response = requests.put(f'{URL.ORDERS_ACCEPT}/1', params=params)

        with allure.step('Проверка ответа'):
            assert response.status_code == 400
            assert response.json()['message'] == TestAnswer.INCOMPLETE_DATA_FOR_SEARCH

    
    @allure.title('Принятие заказа. В запросе указываем неверный id курьера. Проверка тела ответа')
    def test_accept_order_wrong_courier_id_error(self):
        params = {
            "courierId": 0
        }
        with allure.step('Отправка запроса на принятие заказа с указанием неверного id курьера'):
            response = requests.put(f'{URL.ORDERS_ACCEPT}/1', params=params)

        with allure.step('Проверка ответа'):
            assert response.status_code == 404
            assert response.json()['message'] == TestAnswer.COURIER_NOT_EXIST


    @allure.title('Принятие заказа. В запросе не указываем id заказа. Проверка тела ответа')
    def test_accept_order_without_order_id_error (self,create_courier):
        payload_courier = create_courier
        with allure.step('Логин курьера. Получение id курьера'):
            login_courier = requests.post(URL.COURIER_LOGIN, data=payload_courier)
            courier_id = login_courier.json().get('id')

        params = {
            "courierId": courier_id
        }
        with allure.step('Отправка запроса на принятие заказа без указания id заказа'):
            response = requests.put(URL.ORDERS_ACCEPT, params=params)

        with allure.step('Проверка ответа'):
            assert response.status_code == 404
            assert response.json()['message'] == TestAnswer.NOT_FOUND


    @allure.title('Принятие заказа. В запросе указываем неверный id заказа. Проверка тела ответа')
    def test_accept_order_wrong_order_id_error (self,create_courier):
        payload_courier = create_courier
        with allure.step('Логин курьера. Получение id курьера'):
            login_courier = requests.post(URL.COURIER_LOGIN, data=payload_courier)
            courier_id = login_courier.json().get('id')

        params = {
            "courierId": courier_id
        }
        
        with allure.step('Отправка запроса на принятие заказа с указанием неверного id заказа'):
            response = requests.put(f'{URL.ORDERS_ACCEPT}/0', params=params)

        with allure.step('Проверка ответа'):
            assert response.status_code == 404
            assert response.json()['message'] == TestAnswer.ORDER_ID_NOT_EXIST