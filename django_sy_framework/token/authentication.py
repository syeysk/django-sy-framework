from rest_framework import authentication

from django_sy_framework.token.models import Token
from django_sy_framework.custom_auth.utils.crypto import get_hash


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = None
        header_value = request.META.get('HTTP_AUTHORIZATION', '')
        splitted_header_value = header_value.split(' ')
        if len(splitted_header_value) == 2:
            token = splitted_header_value[1]

        if not token:
            return None

        token_object = Token.objects.filter(token=get_hash(token)).first()
        if token_object:
            return token_object.user, token
