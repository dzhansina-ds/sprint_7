import requests
from data import TestData
import allure 
import string
import random
from generator import Generator

class TestAcceptOrder:
    @allure.title('Принятие заказа. Успешный запрос с id курьера и заказа. Проверка тела ответа')
    def test_accept_order_success(self):

        login = Generator().generate_random_string(10)
        password = Generator().generate_random_string(10)
        first_name = Generator().generate_random_string(10)

        payload_courier = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        create_courier = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload_courier)
        login_courier = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload_courier)
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
        make_order = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', json=payload_order)
        track_number = make_order.json().get("track")
        order_data={"t": track_number}
        get_order_info = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders/track', params=order_data)
        order_id = get_order_info.json().get('order').get('id')


        params = {
            "courierId": courier_id
        }

        response = requests.put(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/{order_id}', params=params)

        assert response.status_code == 200
        assert response.json() == {"ok":True}

        requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')


    @allure.title('Принятие заказа. В запросе не указываем id курьера. Проверка тела ответа')
    def test_accept_order_without_courier_id_error(self):
        params = {}

        response = requests.put('https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/1', params=params)

        assert response.status_code == 400
        assert response.json()['message'] == "Недостаточно данных для поиска"

    
    @allure.title('Принятие заказа. В запросе указываем неверный id курьера. Проверка тела ответа')
    def test_accept_order_wrong_courier_id_error(self):
        params = {
            "courierId": 0
        }

        response = requests.put('https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/1', params=params)

        assert response.status_code == 404
        assert response.json()['message'] == "Курьера с таким id не существует"


    @allure.title('Принятие заказа. В запросе не указываем id заказа. Проверка тела ответа')
    def test_accept_order_without_order_id_error (self):

        login = Generator().generate_random_string(10)
        password = Generator().generate_random_string(10)
        first_name = Generator().generate_random_string(10)

        payload_courier = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        create_courier = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload_courier)
        login_courier = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload_courier)
        courier_id = login_courier.json().get('id')

        params = {
            "courierId": courier_id
        }

        response = requests.put('https://qa-scooter.praktikum-services.ru/api/v1/orders/accept', params=params)

        assert response.status_code == 404
        assert response.json()['message'] == "Not Found."


    @allure.title('Принятие заказа. В запросе указываем неверный id заказа. Проверка тела ответа')
    def test_accept_order_wrong_order_id_error (self):

        login = Generator().generate_random_string(10)
        password = Generator().generate_random_string(10)
        first_name = Generator().generate_random_string(10)

        payload_courier = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        create_courier = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload_courier)
        login_courier = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload_courier)
        courier_id = login_courier.json().get('id')

        params = {
            "courierId": courier_id
        }

        response = requests.put('https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/0', params=params)

        assert response.status_code == 404
        assert response.json()['message'] == "Заказа с таким id не существует"

        requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
