from django.urls import path

from django_sy_framework.linker.views import LinkerCreateView, LinkerGetView


urlpatterns = [
    path('get/<str:link_to>/<int:link_to_id>/', LinkerGetView.as_view(), name='linker_objects_get'),
    path('create/<str:link_to>/<int:link_to_id>/', LinkerCreateView.as_view(), name='linker_objects_create'),
]
