import pytest
import requests
from generator import Generator
from urls import URL

@pytest.fixture
def create_courier():
    payload = {
        "login": Generator().generate_random_string(10),
        "password": Generator().generate_random_string(10),
        "firstName": Generator().generate_random_string(10)
    }
    requests.post(URL.COURIER, data=payload)
    yield payload

    logging = requests.post(URL.COURIER_LOGIN, data=payload)
    courier_id = logging.json().get('id')
    requests.delete(f'{URL.COURIER}/{courier_id}')