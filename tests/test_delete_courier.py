import requests
import allure 
import string
import random

class TestDeleteCourier:

    @allure.title('Удаление курьера. Успешное удаление существующего курьер. Проверка тела ответа')
    def test_delete_courier_success(self):
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        create_courier = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        login_courier = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        courier_id = login_courier.json().get('id')

        
        response = requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')


        assert response.status_code == 200
        assert response.json() == {"ok":True}


    @allure.title('Удаление курьера. Отправка запроса без id. Проверка тела ответа')
    def test_delete_courier_without_id_error(self):
        params_delete = {}
        
        response = requests.delete('https://qa-scooter.praktikum-services.ru/api/v1/courier', params=params_delete)

        assert response.status_code == 404


    @allure.title('Удаление курьера. Отправка запроса с неверным id. Проверка тела ответа')
    def test_delete_courier_wrong_id_error(self):

        response = requests.delete('https://qa-scooter.praktikum-services.ru/api/v1/courier/0')

        assert response.status_code == 404
        assert response.json()['message'] == "Курьера с таким id нет."