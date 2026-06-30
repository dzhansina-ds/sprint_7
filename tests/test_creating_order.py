import requests
from data import TestData
import pytest
import allure 
from urls import URL

class TestCreatingOrder:

    @allure.title('Создание заказа. Использование параметризации для выбора цвета. Проверка тела ответа')
    @pytest.mark.parametrize (
        'color',
        [
            ['BLACK'],
            ['GREY'],
            ['BLACK', 'GREY'],
            []
        ]
    )
    def test_set_scooter_colors (self,color):
        payload = {
        "firstName": TestData.firstName,
        "lastName": TestData.lastName,
        "address": TestData.address,
        "metroStation": TestData.metroStation,
        "phone": TestData.phone,
        "rentTime": TestData.rentTime,
        "deliveryDate": TestData.deliveryDate,
        "comment": TestData.comment,
        "color": color
    }
        
        response = requests.post(URL.ORDERS, json=payload)

        assert response.status_code == 201
        assert 'track' in response.json()