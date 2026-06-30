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
        first_response = requests.post(URL.ORDERS, json=payload)
        track_number = first_response.json().get("track")
        params={"t": track_number}
        second_response = requests.get(URL.ORDERS_TRACK, params=params)

        assert second_response.status_code == 200
        assert 'order' in second_response.json()

    @allure.title('Запрос на получение заказа без номера. Проверка тела ответа')
    def test_get_order_without_number_error(self):
        params = {}
        response = requests.get(URL.ORDERS_TRACK,params=params)

        assert response.status_code == 400
        assert response.json()['message'] == TestAnswer.INCOMPLETE_DATA_FOR_SEARCH

    @allure.title('Запрос на получение заказа с несуществующим заказом. Проверка тела ответа')
    def test_get_order_with_wrong_number_error(self):
        params={"t": 0}
        response = requests.get(URL.ORDERS_TRACK, params=params)

        assert response.status_code == 404
        assert response.json()['message'] == TestAnswer.ORDER_NOT_FOUND