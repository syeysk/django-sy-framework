from django.conf import settings


def settings_variables(request):
    show_metric = True
    if request.user.is_authenticated:
        show_metric = request.user.username not in getattr(settings, 'HIDE_METRIC_FOR', [])

    metric_system_code = getattr(settings, 'METRIC_SYSTEM_CODE', '') if show_metric else ''
    return {
        'metric_system_code': metric_system_code,
        'debug': settings.DEBUG,
        'site_url': settings.SITE_URL,
    }
