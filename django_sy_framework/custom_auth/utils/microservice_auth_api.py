import json
from typing import Any

from django.conf import settings
from django_sy_framework.custom_auth.models import TempTokenModel
from django_sy_framework.custom_auth.utils.crypto import decrypt_text, encrypt_text, get_hash
from rest_framework import serializers
from syapi import auth
from syapi.exceptions import FieldsException


def encrypt_json(json_data):
    return {'data': encrypt_text(json.dumps(json_data))}


def decrypt_json(json_data):
    return json.loads(decrypt_text(json_data['data']))


def save_auth_user(auth_user):
    data = auth_user.serialize()
    user_hash = get_hash(data['microservice_auth_id'])
    token = TempTokenModel.objects.filter(user_hash=user_hash).first()
    if token:
        token.temp_token = data['token']
        token.public_key = data['public_key']
        token.private_key = data['private_key']
        token.auth_public_key = data['auth_public_key']
    else:
        token = TempTokenModel(
            user_hash=user_hash,
            temp_token=data['token'],
            public_key=data['public_key'],
            private_key=data['private_key'],
            auth_public_key=data['auth_public_key'],
        )

    token.save()


def get_auth_user(microservice_auth_id=None):
    microservice_auth_id = str(microservice_auth_id)
    auth_data = {}
    if microservice_auth_id:
        user_hash = get_hash(microservice_auth_id)
        token = TempTokenModel.objects.filter(user_hash=user_hash).first()
        if token:
            auth_data = {
                'microservice_auth_id': microservice_auth_id,
                'token': token.temp_token,
                'public_key': token.public_key.encode(),
                'private_key': token.private_key.encode(),
                'auth_public_key': token.auth_public_key.encode(),
            }

    return auth.User(url=settings.MICROSERVICES_URLS['auth'], **auth_data)


def login(username: str, password: str) -> dict[str, Any] | None:
    """Выполняет авторизацию пользователя. В случае успеха возвращает словарь с данными пользователя"""
    try:
        auth_user = get_auth_user()
        response_data = auth_user.login(username, password)
        save_auth_user(auth_user)
        return response_data
    except FieldsException as error:
        raise serializers.ValidationError(error.errors)


def registrate(username: str, password: str, email: str, first_name: str, last_name: str) -> dict[str, Any] | None:
    """
    Выполняет регистрацию пользователя. В случае успеха возвращает словарь с данными пользователя,
    иначе - словарь с ошибками (подобно сериализатору) либо None
    """
    data = {
        'username': username, 'password': password, 'email': email, 'first_name': first_name, 'last_name': last_name,
    }
    try:
        auth_user = get_auth_user()
        response_data = auth_user.registrate(**data)
        save_auth_user(auth_user)
        return response_data
    except FieldsException as error:
        errors = error.errors
        if 'password' in errors:
            errors['password1'] = errors['password1'] = errors['password']
            del errors['password']

        raise serializers.ValidationError(errors)


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
        'old_token': settings.MICROSERVICES_TOKENS['to_auth']
    }
    auth_user = get_auth_user()
    response_data = auth_user.login_or_registrate_by_extern(**data)
    save_auth_user(auth_user)
    return response_data


def edit(
    microservice_auth_id: 'uuid.UUID',
    username: str,
    last_name: str,
    first_name: str,
) -> dict:
    """Выполняет изменение данных пользователя. В случае успеха возвращает пустой словарь"""
    data = {
        'username': username,
        'last_name': last_name,
        'first_name': first_name,
    }
    try:
        response_data = get_auth_user(microservice_auth_id).put(**data)
        return response_data['updated_fields']
    except FieldsException as error:
        raise serializers.ValidationError(error.errors)


def get(microservice_auth_id: 'uuid.UUID') -> dict:
    """Выполняет получение данных пользователя."""
    response_data = get_auth_user(microservice_auth_id).get()
    return {
        'username': response_data['username'],
        'last_name': response_data['last_name'],
        'first_name': response_data['first_name'],
        'is_staff': response_data['is_staff'],
        'is_active': response_data['is_active'],
        'is_superuser': response_data['is_superuser'],
        'email': response_data['email'],
    }


def delete(microservice_auth_id: 'uuid.UUID') -> dict:
    """Выполняет получение данных пользователя."""
    get_auth_user(microservice_auth_id).delete()
