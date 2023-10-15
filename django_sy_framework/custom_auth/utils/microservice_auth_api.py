import json
from typing import Any

from django_sy_framework.custom_auth.utils.crypto import decrypt_text, encrypt_text
from django_sy_framework.utils.universal_api import API


def encrypt_json(json_data):
    return {'data': encrypt_text(json.dumps(json_data))}


def decrypt_json(json_data):
    return json.loads(decrypt_text(json_data['data']))


def login(username: str, password: str) -> dict[str, Any] | None:
    """Выполняет авторизацию пользователя. В случае успеха возвращает словарь с данными пользователя"""
    api = API('1', 'auth')
    data = {'username': username, 'password': password}
    response = api.auth.login.post('/', json=encrypt_json(data))
    if response.status_code == 200:
        response_data = decrypt_json(response.json())
        if response_data['success']:
            return {
                'microservice_auth_id': response_data['microservice_auth_id'],
                'last_name': response_data['last_name'],
                'first_name': response_data['first_name'],
                'is_staff': response_data['is_staff'],
                'is_active': response_data['is_active'],
                'is_superuser': response_data['is_superuser'],
            }


def registrate(username: str, password: str, email: str, first_name: str, last_name: str) -> dict[str, Any] | None:
    """
    Выполняет регистрацию пользователя. В случае успеха возвращает словарь с данными пользователя,
    иначе - словарь с ошибками (подобно сериализатору) либо None
    """
    data = {
        'username': username, 'password': password, 'email': email, 'first_name': first_name, 'last_name': last_name,
    }
    api = API('1', 'auth')
    response = api.auth.registrate.post('/', json=encrypt_json(data))
    if response.status_code == 200:
        response_data = decrypt_json(response.json())
        if response_data['success']:
            return {'microservice_auth_id': response_data['microservice_auth_id']}
    elif response.status_code == 400:
        return decrypt_json(response.json())


def login_or_registrate_by_extern_service(
    username_for_new_user: str,
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
        'username': username_for_new_user,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'extern_id': extern_id,
    }
    api = API('1', 'auth')
    response = api.auth.login_or_registrate_by_extern.post('/', json=encrypt_json(data))
    if response.status_code == 200:
        response_data = decrypt_json(response.json())
        if response_data['success']:
            return {
                'microservice_auth_id': response_data['microservice_auth_id'],
                'username': response_data['username'],
                'last_name': response_data['last_name'],
                'first_name': response_data['first_name'],
                'is_staff': response_data['is_staff'],
                'is_active': response_data['is_active'],
                'is_superuser': response_data['is_superuser'],
            }


def edit(
    microservice_auth_id: 'uuid.UUID',
    username: str,
    last_name: str,
    first_name: str,
) -> dict:
    """Выполняет изменение данных пользователя. В случае успеха возвращает пустой словарь"""
    data = {
        'microservice_auth_id': str(microservice_auth_id),
        'username': username,
        'last_name': last_name,
        'first_name': first_name,
    }
    api = API('1', 'auth')
    response = api.auth.user.put('/', json=encrypt_json(data))
    if response.status_code == 200:
        response_data = decrypt_json(response.json())
        if response_data['success']:
            return response_data['updated_fields']


def get(microservice_auth_id: 'uuid.UUID') -> dict:
    """Выполняет получение данных пользователя."""
    data = {'microservice_auth_id': str(microservice_auth_id)}
    api = API('1', 'auth')
    response = api.auth.user.get('/', json=encrypt_json(data))
    if response.status_code == 200:
        response_data = decrypt_json(response.json())
        if response_data['success']:
            return {
                'username': response_data['username'],
                'last_name': response_data['last_name'],
                'first_name': response_data['first_name'],
                'is_staff': response_data['is_staff'],
                'is_active': response_data['is_active'],
                'is_superuser': response_data['is_superuser'],
                'email': response_data['email'],
            }


def delete(microservice_auth_id: 'uuid.UUID', password: str) -> dict:
    """Выполняет получение данных пользователя."""
    data = {'microservice_auth_id': str(microservice_auth_id), 'password': password}
    api = API('1', 'auth')
    response = api.auth.user.delete('/', json=encrypt_json(data))
    if response.status_code == 200:
        response_data = decrypt_json(response.json())
        return response_data['success']
