import requests
import allure 
from urls import URL

class TestOrdersList:
    @allure.title('Список заказов. Проверка тела ответа на содержание списка заказов')
    def test_get_order_list(self):
       
        response = requests.get(URL.ORDERS)

        assert response.status_code == 200 
        assert 'orders' in response.json()