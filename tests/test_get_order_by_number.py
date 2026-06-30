from data import TestData, TestAnswer
import requests
import allure 
from urls import URL


class TestGetOrderByNumber:
    @allure.title('Успешное получение заказа по его номеру. Проверка тела ответа')
    def test_get_order_by_number_success(self):
        payload = {
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
        with allure.step('Создание заказа. Получение трек-номера'):
            first_response = requests.post(URL.ORDERS, json=payload)
            track_number = first_response.json().get("track")
        
        with allure.step('Получение информации о заказе с помощью трек-номера'):
            params={"t": track_number}
            second_response = requests.get(URL.ORDERS_TRACK, params=params)
        
        with allure.step('Проверка ответа'):
            assert second_response.status_code == 200
            assert 'order' in second_response.json()

    @allure.title('Запрос на получение заказа без номера. Проверка тела ответа')
    def test_get_order_without_number_error(self):
        
        with allure.step('Отправка запроса о получении информации о заказе без трек-номера'):
            params = {}
            response = requests.get(URL.ORDERS_TRACK,params=params)
        
        with allure.step('Проверка ответа'):
            assert response.status_code == 400
            assert response.json()['message'] == TestAnswer.INCOMPLETE_DATA_FOR_SEARCH

    @allure.title('Запрос на получение заказа с несуществующим номером. Проверка тела ответа')
    def test_get_order_with_wrong_number_error(self):
        
        with allure.step('Отправка запроса о получении информации о заказе с несуществующим трек-номером'):
            params={"t": 0}
            response = requests.get(URL.ORDERS_TRACK, params=params)
        
        with allure.step('Проверка ответа'):
            assert response.status_code == 404
            assert response.json()['message'] == TestAnswer.ORDER_NOT_FOUND