class TestData:
    valid_login = 'ninja'
    valid_password = '1234'
    invalid_login = 'ninja13x13'
    invalid_password = '12xx34xx'
    firstName = 'Brock'
    lastName ='Lesnar'
    address = '1221 SW 4th Ave, Portland'
    metroStation = 4
    phone = '+78003553535'
    rentTime = 5
    deliveryDate = '2020-07-07' 
    comment = 'Welcome to the RIP City'    

class TestAnswer:
    SUCCESS_TEXT = {"ok":True}
    INCOMPLETE_DATA_FOR_SEARCH = "Недостаточно данных для поиска"
    COURIER_NOT_EXIST = "Курьера с таким id не существует"
    NOT_FOUND = "Not Found."
    ORDER_ID_NOT_EXIST = "Заказа с таким id не существует"
    BUSY_USERNAME = "Этот логин уже используется. Попробуйте другой."
    COURIER_INCOMPLETE_DATA = "Недостаточно данных для создания учетной записи"
    COURIER_NOT_FOUND = "Курьера с таким id нет."
    ORDER_NOT_FOUND = "Заказ не найден"
    INCOMPLETE_DATA_FOR_ENTER = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
