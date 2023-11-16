from django.urls import path
from django.views.generic.base import TemplateView

from django_sy_framework.custom_auth.views import (
    ExternAuthGoogleView,
    LoginView,
    LogoutView,
    RegistrationView,
)

urlpatterns = [
    path('want_to_go_in', TemplateView.as_view(template_name='custom_auth/login.html'), name='custom_login_page'),
    path(
        'want_to_be_a_user',
         TemplateView.as_view(template_name='custom_auth/registrate.html'),
        name='custom_registration_page',
    ),
    path('login', LoginView.as_view(), name='custom_login'),
    path('logout', LogoutView.as_view(), name='custom_logout'),
    path('registrate', RegistrationView.as_view(), name='custom_registration'),
    path('extern_google', ExternAuthGoogleView.as_view(), name='extern_auth_google'),
]
