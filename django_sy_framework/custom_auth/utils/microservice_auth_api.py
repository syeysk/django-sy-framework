import json
from typing import Any

import requests
from django.conf import settings

from django_sy_framework.custom_auth.utils.crypto import decrypt_text, encrypt_text


def encrypt_json(json_data):
    return {'data': encrypt_text(json.dumps(json_data))}


def decrypt_json(json_data):
    return json.loads(decrypt_text(json_data['data']))


class MethodAPI:
    def __init__(self, api_version, microservice_name, api_method):
        self.microservice_name = microservice_name
        self.api_version = api_version
        self.api_method = api_method

    def __getattr__(self, method_str):
        token = settings.MICROSERVICES_TOKENS[f'to_{self.microservice_name}']
        microservice_url = settings.MICROSERVICES_URLS[self.microservice_name]
        url = f'{microservice_url}/api/v{self.api_version}/{self.microservice_name}/{self.api_method}'
        method = getattr(requests, method_str)

        def get_request_func(path, **kwargs):
            headers = kwargs.setdefault('headers', {})
            headers['AUTHORIZATION'] = f'Token {token}'
            return method(f'{url}{path}', **kwargs)

        return get_request_func


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
    data = {'username': username, 'password': password}
    response = api.auth.login.post('/', json=encrypt_json(data))
    if response.status_code == 200:
        responsed_data = decrypt_json(response.json())
        if responsed_data['success']:
            return {
                'microservice_auth_id': responsed_data['microservice_auth_id'],
                'last_name': responsed_data['last_name'],
                'first_name': responsed_data['first_name'],
                'is_staff': responsed_data['is_staff'],
                'is_active': responsed_data['is_active'],
                'is_superuser': responsed_data['is_superuser'],
            }


def registrate(username: str, password: str, email: str, first_name: str, last_name: str) -> dict[str, Any] | None:
    """
    Выполняет регистрацию пользователя. В случае успеха возвращает словарь с данными пользователя,
    иначе - словарь с ошибками (подобно сериализатору) либо None
    """
    data = {
        'username': username, 'password': password, 'email': email, 'first_name': first_name, 'last_name': last_name,
    }
    api = FullAPI('1')
    response = api.auth.registrate.post('/', json=encrypt_json(data))
    if response.status_code == 200:
        responsed_data = decrypt_json(response.json())
        if responsed_data['success']:
            return {'microservice_auth_id': responsed_data['microservice_auth_id']}
    elif response.status_code == 400:
        return decrypt_json(response.json())


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
    response = api.auth.login_or_registrate_by_extern.post('/', json=encrypt_json(data))
    if response.status_code == 200:
        responsed_data = decrypt_json(response.json())
        if responsed_data['success']:
            return {
                'microservice_auth_id': responsed_data['microservice_auth_id'],
                'last_name': responsed_data['last_name'],
                'first_name': responsed_data['first_name'],
                'is_staff': responsed_data['is_staff'],
                'is_active': responsed_data['is_active'],
                'is_superuser': responsed_data['is_superuser'],
            }


def delete(username: str, password: str) -> dict:
    """
    Выполняет удаление пользователя.
    :param username: имя пользователя
    :param password: пароль пользователя
    :return: в случае успеха возвращает пустой словарь, иначе - данные с ошибками в формате, как у сериалиазатора"""
    data = {}
    api = FullAPI('1')
    response = api.auth.user.delete('/', json=encrypt_json(data))
    return {}


def edit(
    current_username: str,
    username: str,
    last_name: str,
    first_name: str,
) -> dict:
    """Выполняет изменение данных пользователя. В случае успеха возвращает пустой словарь"""
    data = {
        'current_username': current_username,
        'username': username,
        'last_name': last_name,
        'first_name': first_name,
    }
    api = FullAPI('1')
    response = api.auth.user.put('/', json=encrypt_json(data))
    if response.status_code == 200:
        responsed_data = decrypt_json(response.json())
        if responsed_data['success']:
            return responsed_data['updated_fields']


def get(username: str) -> dict:
    """Выполняет получение данных пользователя."""
    data = {'username': username}
    api = FullAPI('1')
    response = api.auth.user.get('/', json=encrypt_json(data))
    if response.status_code == 200:
        responsed_data = decrypt_json(response.json())
        if responsed_data['success']:
            return {
                'last_name': responsed_data['last_name'],
                'first_name': responsed_data['first_name'],
                'is_staff': responsed_data['is_staff'],
                'is_active': responsed_data['is_active'],
                'is_superuser': responsed_data['is_superuser'],
                'email': responsed_data['email'],
            }
