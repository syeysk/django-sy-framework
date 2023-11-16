from django.urls import path

from django_sy_framework.token.views import (
    AddTokenView,
    DeleteTokenView,
    EditTokenView,
    TokenView,
)

urlpatterns = [
    path('', TokenView.as_view(), name='custom_auth_tokens'),
    path('add', AddTokenView.as_view(), name='custom_auth_add_token'),
    path('edit', EditTokenView.as_view(), name='custom_auth_edit_token'),
    path('delete/<int:pk>', DeleteTokenView.as_view(), name='custom_auth_delete_token'),
]
