from django.conf import settings


def settings_variables(request):
    show_metric = True
    if request.user.is_authenticated:
        show_metric = request.user.username not in getattr(settings, 'HIDE_METRIC_FOR', [])

    metric_system_code = getattr(settings, 'METRIC_SYSTEM_CODE', '') if show_metric else ''
    is_i18n_on = bool(getattr(request, 'LANGUAGE_CODE', ''))
    return {
        'metric_system_code': metric_system_code,
        'debug': settings.DEBUG,
        'site_url': settings.SITE_URL,
        'is_i18n_on': is_i18n_on,
        'user_lang_code': request.LANGUAGE_CODE if is_i18n_on else settings.LANGUAGE_CODE,
    }
