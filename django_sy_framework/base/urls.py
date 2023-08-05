from django.urls import path

from .views import (
    IntroView,
    MicroservicesListView,
    ProfileView,
    ServiceServerView,
)


urlpatterns = [
    path('', IntroView.as_view(), name='index'),
    path('all-microservices/', MicroservicesListView.as_view(), name='microservices'),
    path('profile/', ProfileView.as_view(), name='custom_profile'),
    path('service_server/', ServiceServerView.as_view(), name='service_server'),
]
