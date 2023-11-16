from django.apps import AppConfig


class TokenConfig(AppConfig):
    # default_auto_field = "django.db.models.BigAutoField"
    name = 'django_sy_framework.token'

    def ready(self):
        import django_sy_framework.token.schema  # noqa: E402
