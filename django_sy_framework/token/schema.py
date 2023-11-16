from drf_spectacular.extensions import OpenApiAuthenticationExtension

from django_sy_framework.token.authentication import TokenAuthentication


class Auth(OpenApiAuthenticationExtension):
    name = 'Token authentication'
    target_class = TokenAuthentication

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'name': 'AUTHORIZATION',
            'in': 'header',
            'scheme': 'Bearer',
        }