import json

from django.conf import settings
from django_sy_framework.custom_auth.models import TempTokenModel
from django_sy_framework.custom_auth.utils.crypto import decrypt_text, encrypt_text, get_hash
from syapi import auth


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
