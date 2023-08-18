from typing import Any

import requests
from django.conf import settings


class MethodAPI:
    def __init__(self, api_version, microservice_name, api_method):
        self.microservice_name = microservice_name
        self.api_version = api_version
        self.api_method = api_method

    def __getattr__(self, method_str):
        salt = settings.MICROSERVICES_KEYS[self.microservice_name]
        microservice_url = settings.MICROSERVICES_URLS[self.microservice_name]
        url = f'{microservice_url}/api/v{self.api_version}/{self.microservice_name}/{self.api_method}'
        method = getattr(requests, method_str)
        return lambda path='', **kwargs: method(f'{url}{path}', **kwargs)


class MicroserviceAPI:
    def __init__(self, api_version, microservice_name):
        self.microservice_name = microservice_name
        self.api_version = api_version

    def __getattr__(self, api_method):
        return MethodAPI(self.api_version, self.microservice_name, api_method)


class FullAPI:
    def __init__(self, api_version):
        self.api_version = api_version

    def __getattr__(self, microservice_name):
        return MicroserviceAPI(self.api_version, microservice_name)


def login(username: str, password: str) -> dict[str, Any] | None:
    """Выполняет авторизацию пользователя. В случае успеха возвращает словарь с данными пользователя"""
    api = FullAPI('1')
    response = api.auth.login.post('/', json={'username': username, 'password': password})
    if response.status_code == 200:
        responsed_data = response.json()
        if responsed_data['success']:
            return {
                'microservice_auth_id': responsed_data['microservice_auth_id'],
                'last_name': responsed_data['last_name'],
                'first_name': responsed_data['first_name'],
                'is_staff': responsed_data['is_staff'],
                'is_superuser': responsed_data['is_superuser'],
            }


def registrate(username: str, password: str, email: str, first_name: str, last_name: str) -> dict[str, Any] | None:
    """Выполняет регистрацию пользователя. В случае успеха возвращает словарь с данными пользователя"""
    data = {
        'username': username, 'password': password, 'email': email, 'first_name': first_name, 'last_name': last_name,
    }
    api = FullAPI('1')
    response = api.auth.registrate.post('/', json=data)
    if response.status_code == 200:
        responsed_data = response.json()
        if responsed_data['success']:
            return {'microservice_auth_id': responsed_data['microservice_auth_id']}


def login_or_registrate_by_extern_service(
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    extern_id: str,
) -> dict:
    """
    Выполняет авторизацию пользователя через внешний сервис. Например, Google.
    Если пользователя не существует - регистрирует.
    В случае успеха возвращает словарь с данными пользователя
    """
    data = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'extern_id': extern_id,
    }
    api = FullAPI('1')
    response = api.auth.login_or_registrate_by_extern.post('/', json=data)
    if response.status_code == 200:
        responsed_data = response.json()
        if responsed_data['success']:
            return {
                'microservice_auth_id': responsed_data['microservice_auth_id'],
                'last_name': responsed_data['last_name'],
                'first_name': responsed_data['first_name'],
                'is_staff': responsed_data['is_staff'],
                'is_superuser': responsed_data['is_superuser'],
            }


def delete(username: str, password: str) -> dict:
    """
    Выполняет удаление пользователя.
    :param username: имя пользователя
    :param password: пароль пользователя
    :return: в случае успеха возвращает пустой словарь, иначе - данные с ошибками в формате, как у сериалиазатора"""
    api = FullAPI('1')
    response = api.auth.user.delete('/', json={})
    return {}


def edit(username: str, user_data: dict) -> dict:
    """Выполняет изменение данных пользователя. В случае успеха возвращает пустой словарь"""
    api = FullAPI('1')
    response = api.auth.user.put('/', json={})
    return {}


def get(username: str, user_data: dict) -> dict:
    """Выполняет получение данных пользователя."""
    api = FullAPI('1')
    response = api.auth.user.get('/', json={})
    return {}
