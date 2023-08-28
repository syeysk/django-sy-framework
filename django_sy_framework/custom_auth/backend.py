from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from django_sy_framework.utils import microservice_auth_api


def create_or_update_user(**user_data) -> 'django_sy_framework.custom_auth.CustomAuthUser':
    """
    Функция создаёт либо обновляет локального пользователя
    :param user_data: данные глобального пользователя
    :return: возвращает локального пользователя
    """
    user_model = get_user_model()
    microservice_auth_id = user_data['microservice_auth_id']
    user = user_model.objects.filter(microservice_auth_id=microservice_auth_id).first()
    if user:
        fields_to_update = []
        if user.username != user_data['username']:
            user.username = user_data['username']
            fields_to_update.append('username')

        if user.last_name != user_data['last_name']:
            user.last_name = user_data['last_name']
            fields_to_update.append('last_name')

        if user.first_name != user_data['first_name']:
            user.first_name = user_data['first_name']
            fields_to_update.append('first_name')

        if user.first_name != user_data['is_staff']:
            user.is_staff = user_data['is_staff']
            fields_to_update.append('is_staff')

        if user.is_superuser != user_data['is_superuser']:
            user.is_superuser = user_data['is_superuser']
            fields_to_update.append('is_superuser')

        if fields_to_update:
            user.save(update_fields=fields_to_update)
    else:
        user = user_model(
            microservice_auth_id=microservice_auth_id,
            username=user_data['username'],
            last_name=user_data['last_name'],
            first_name=user_data['first_name'],
            is_staff=user_data['is_staff'],
            is_superuser=user_data['is_superuser'],
        )
        user.save()

    return user


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        user_data = microservice_auth_api.login(username, password)
        if user_data:
            return create_or_update_user(username=username, **user_data)

    def get_user(self, user_id):
        user_model = get_user_model()
        return user_model.objects.filter(pk=user_id).first()
