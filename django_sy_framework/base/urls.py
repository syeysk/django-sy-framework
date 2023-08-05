from django.urls import path

from .views import (
    IntroView,
    MicroservicesListView,
)


urlpatterns = [
    path('', IntroView.as_view(), name='index'),
    path('all-microservices/', MicroservicesListView.as_view(), name='microservices'),
]
