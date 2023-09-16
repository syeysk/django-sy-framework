from django.urls import path

from django_sy_framework.linker.views import LinkerView


urlpatterns = [
    path('<str:link_to>/<int:link_to_id>/', LinkerView.as_view(), name='linker_objects'),
]
