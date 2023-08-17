from django.apps import AppConfig
from django.conf import settings


class CustomAuthConfig(AppConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        constant_names = [
            'EXTERN_AUTH',
        ]
        for constant_name in constant_names:
            getattr(settings, constant_name)
