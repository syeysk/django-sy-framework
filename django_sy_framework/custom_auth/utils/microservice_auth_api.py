from typing import Any

import requests
from django.conf import settings


def login(username: str, password: str) -> dict[str, Any] | None:
    """Выполняет авторизацию пользователя. В случае успеха возвращает словарь с данными пользователя"""
    token = settings.MICROSERVICES_TOKENS['to_auth']
    salt = settings.MICROSERVICES_KEYS['auth']
    url = '{}/api/v1/auth/login/'.format(settings.MICROSERVICES_URLS['auth'])
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
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
    token = settings.MICROSERVICES_TOKENS['to_auth']
    salt = settings.MICROSERVICES_KEYS['auth']
    url = '{}/api/v1/auth/registrate/'.format(settings.MICROSERVICES_URLS['auth'])
    data = {
        'username': username, 'password': password, 'email': email, 'first_name': first_name, 'last_name': last_name,
    }
    response = requests.post(url, json=data)
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
    token = settings.MICROSERVICES_TOKENS['to_auth']
    salt = settings.MICROSERVICES_KEYS['auth']
    url = '{}/api/v1/auth/login_or_registrate_by_extern/'.format(settings.MICROSERVICES_URLS['auth'])
    data = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'extern_id': extern_id,
    }
    response = requests.post(url, json=data)
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
    token = settings.MICROSERVICES_TOKENS['to_auth']
    salt = settings.MICROSERVICES_KEYS['auth']
    url = '{}/api/v1/auth/user/'.format(settings.MICROSERVICES_URLS['auth'])
    response = requests.delete(url)
    return {}


def edit(username: str, user_data: dict) -> dict:
    """Выполняет изменение данных пользователя. В случае успеха возвращает пустой словарь"""
    token = settings.MICROSERVICES_TOKENS['to_auth']
    salt = settings.MICROSERVICES_KEYS['auth']
    url = '{}/api/v1/auth/user/'.format(settings.MICROSERVICES_URLS['auth'])
    response = requests.put(url)
    return {}


def get(username: str, user_data: dict) -> dict:
    """Выполняет получение данных пользователя."""
    token = settings.MICROSERVICES_TOKENS['to_auth']
    salt = settings.MICROSERVICES_KEYS['auth']
    url = '{}/api/v1/auth/user/'.format(settings.MICROSERVICES_URLS['auth'])
    response = requests.get(url)
    return {}
