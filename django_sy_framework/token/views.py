from secrets import token_urlsafe

from django.contrib.auth import mixins
from django.shortcuts import render
from django.views import View
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django_sy_framework.custom_auth.utils.crypto import get_hash
from django_sy_framework.token.authentication import TokenAuthentication
from django_sy_framework.token.models import Token
from django_sy_framework.token.permissions import CheckIsUsernNotAnonymousUser
from django_sy_framework.token.serializers import (
    AddTokenSerializer,
    EditTokenSerializer,
)


class AllowAnyMixin:
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [AllowAny]


class LoginRequiredMixin:
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [CheckIsUsernNotAnonymousUser]


class TokenView(mixins.LoginRequiredMixin, View):
    def get(self, request):
        tokens = Token.objects.filter(user=request.user).values('id', 'app_name')
        context = {'tokens': list(tokens)}
        return render(request, 'token/tokens.html', context=context)


class AddTokenView(mixins.LoginRequiredMixin, APIView):
    def post(self, request):
        serializer = AddTokenSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        token_str_source = token_urlsafe(64)
        token_str_hashed = get_hash(token_str_source)
        token = Token(user=request.user, app_name=data['app_name'], token=token_str_hashed)
        token.save()
        data_for_response = {
            'id': token.pk,
            'token': token_str_source,
        }
        return Response(status=status.HTTP_200_OK, data=data_for_response)


class EditTokenView(mixins.LoginRequiredMixin, APIView):
    def post(self, request):
        serializer = EditTokenSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        token = Token.objects.get(user=request.user, pk=data['token_id'])
        token.app_name = data['app_name']
        token.save()
        data_for_response = {}
        return Response(status=status.HTTP_200_OK, data=data_for_response)


class DeleteTokenView(mixins.LoginRequiredMixin, APIView):
    def post(self, request, pk):
        token = Token.objects.get(user=request.user, pk=pk)
        token.delete()
        data_for_response = {}
        return Response(status=status.HTTP_200_OK, data=data_for_response)
