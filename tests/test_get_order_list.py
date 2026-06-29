import requests
import allure 

class TestOrdersList:
    @allure.title('Список заказов. Проверка тела ответа на содержание списка заказов')
    def test_get_order_list(self):
       
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders')

        assert response.status_code == 200 
        assert 'orders' in response.json()