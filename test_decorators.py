from my_decorator import do_twice

@do_twice
def twice_without_params():
    print("Этот вызов без параметров")
@do_twice
def twice_2_params(str1, str2):
    print("В этой функции 2 параметра - {0} и {1}".format(str1, str2))
@do_twice
def twice(str):
    print("Этот вызов возвращает строку {0}".format(str))

twice_without_params()
twice_2_params("1", "2")
twice("single")

def do_twice(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
      func(*args, **kwargs)
      return func(*args, **kwargs)
  return wrapper


import functools

print(twice.__name__)

def debug(func):
    """Выводит сигнатуру функции и возвращаемое значение"""
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Вызываем {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} вернула значение - {value!r}")
        return value
    return wrapper_debug
@debug
def age_passed(name, age=None):
  if age is None:
    return "Необходимо передать значение age"
  else:
    return "Аргументы по умолчанию заданы!"

age_passed("Роман")
age_passed("Роман", age=21)



import pytest
import requests
import json




from conftest import get_key


@pytest.fixture()
def some_data():
    return 42

def test_some_data(some_data):
     assert some_data == 42


# def get_key():
    # переменные email и password нужно заменить своими учетными данными
   # response = requests.post(url='https://petfriends.skillfactory.ru/login',
   #                          data={"email": email, "pass": password})
   # assert response.status_code == 200, 'Запрос выполнен неуспешно'
   # assert 'Cookie' in response.request.headers, 'В запросе не передан ключ авторизации'
   # return response.request.headers.get('Cookie')


def test_getAllPets(get_key):
    response = requests.get(url='https://petfriends.skillfactory.ru/api/pets',
                            headers={"Cookie": get_key})
    assert response.status_code == 200, 'Запрос выполнен неуспешно'
    assert len(response.json().get('pets')) > 0, 'Количество питомцев не соответствует ожиданиям'

from datetime import datetime
@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print (f"\nТест шел: {end_time - start_time}")





def session_fixture():
    print('\nclass fixture starts')

@pytest.fixture(scope="function", autouse=True)
def function_fixture():
    print("\nfunction fixture starts")


class TestClass23:

    def test_first(self):
        pass

    def test_second(self):
        pass


#При запуске нашего теста на экран должны вывестись:
#-Название нашей фикстуры, её область видимости, название теста, название класса,
#-Название модуля и путь до файлика, из которого запущен наш тест.
#-Последней строкой выводится информация о том, запущен ли наш тест из класса или нет.

@pytest.fixture()
def request_fixture(request):
    print(request.fixturename)
    print(request.scope)
    print(request.function.__name__)
    print(request.cls)
    print(request.module.__name__)
    print(request.fspath)
    if request.cls:
        return f"\n У теста {request.function.__name__} класс есть\n"
    else:
        return f"\n У теста {request.function.__name__} класса нет\n"


def test_request_1(request_fixture):
    print(request_fixture)


class TestClassRequest:

    def test_request_2(self, request_fixture):
        print(request_fixture)



#########

import pytest
import requests

from conftest import email, password

@pytest.fixture(scope="class")
def get_key(request):
    # переменные email и password нужно заменить своими учетными данными
    response = requests.post(url='https://petfriends.skillfactory.ru/login',
                             data={"email": email, "pass": password})
    assert response.status_code == 200, 'Запрос выполнен неуспешно'
    assert 'Cookie' in response.request.headers, 'В запросе не передан ключ авторизации'
    print("\nreturn auth_key")
    return response.request.headers.get('Cookie')


@pytest.fixture(autouse=True)
def request_fixture(request):
    if 'Pets' in request.function.__name__:
        print(f"\nЗапущен тест из сьюта Дом Питомца: {request.function.__name__}")


class TestClassPets:

    def test_getAllPets2(self, get_key):
        response = requests.get(url='https://petfriends.skillfactory.ru/api/pets',
                                headers={"Cookie": get_key})
        assert response.status_code == 200, 'Запрос выполнен неуспешно'
        assert len(response.json().get('pets')) > 0, 'Количество питомцев не соответствует ожиданиям'

    def test_getMyPets2(self, get_key):
        response = requests.get(url='https://petfriends.skillfactory.ru/my_pets',
                                headers={"Cookie": get_key})
        assert response.status_code == 200, 'Запрос выполнен неуспешно'
        assert response.headers.get('Content-Type') == 'text/html; charset=utf-8'

    def test_anotherTest(self):
        pass