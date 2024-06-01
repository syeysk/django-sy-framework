ROOT_URLCONF = 'server.urls'
WSGI_APPLICATION = 'server.wsgi.application'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
INTERNAL_IPS = ['127.0.0.1']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'custom_auth.CustomAuthUser'
AUTHENTICATION_BACKENDS = ['django_sy_framework.custom_auth.backend.CustomAuthBackend']
LOGIN_URL = 'custom_login_page'
GO_HERE_AFTER_LOGING = 'index'
GO_HERE_AFTER_REGISTRATION = 'index'
