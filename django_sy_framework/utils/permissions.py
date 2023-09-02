from django.conf import settings
from rest_framework.permissions import BasePermission


class IsRequestFromMicroservice(BasePermission):
    """Class for checking permissions by token between Platform's microservices"""
    def has_permission(self, request, view):
        return request.auth in set(settings.MICROSERVICES_TOKENS.values())  # TODO: реализовать нормально!
