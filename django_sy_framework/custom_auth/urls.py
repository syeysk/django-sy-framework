from django.urls import path, re_path
from django.views.generic.base import TemplateView

from django_sy_framework.custom_auth.views import (
    AddTokenView,
    DeleteTokenView,
    EditTokenView,
    ExternAuthGoogleView,
    LoginView,
    LogoutView,
    TokenView,
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
    path('token/', TokenView.as_view(), name='custom_auth_tokens'),
    path('token/add', AddTokenView.as_view(), name='custom_auth_add_token'),
    path('token/edit', EditTokenView.as_view(), name='custom_auth_edit_token'),
    re_path('token/delete/(?P<pk>[0-9]+)$', DeleteTokenView.as_view(), name='custom_auth_delete_token'),
]
