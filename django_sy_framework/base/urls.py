from django.urls import path

from django_sy_framework.base.views import (
    IntroView,
    MicroservicesListView,
    ProfileView,
    RobotsTxtView,
    ServiceServerView,
)


urlpatterns = [
    path('', IntroView.as_view(), name='index'),
    path('all-microservices/', MicroservicesListView.as_view(), name='microservices'),
    path('profile/', ProfileView.as_view(), name='custom_profile'),
    path('service_server/', ServiceServerView.as_view(), name='service_server'),
    path('robots.txt', RobotsTxtView.as_view(), name='robots_txt'),
]
