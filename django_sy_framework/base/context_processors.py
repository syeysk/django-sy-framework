from django.conf import settings


def settings_variables(request):
    return {
        'metric_system_code': getattr(settings, 'METRIC_SYSTEM_CODE', ''),
        'debug': settings.DEBUG,
        'site_url': settings.SITE_URL,
    }
