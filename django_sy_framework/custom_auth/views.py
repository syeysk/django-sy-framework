import requests
from secrets import token_urlsafe

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from requests.exceptions import ConnectionError
from syapi.exceptions import FieldsException

from django_sy_framework.custom_auth.models import Token
from django_sy_framework.custom_auth.serializers import (
    AddTokenSerializer,
    EditTokenSerializer,
    RegistrationSerializer,
)
from django_sy_framework.custom_auth.backend import create_or_update_user
from django_sy_framework.custom_auth.utils import microservice_auth_api
from django_sy_framework.custom_auth.utils.crypto import get_hash


def create_user(**user_data):
    user_model = get_user_model()
    user = user_model(
        microservice_auth_id=user_data['microservice_auth_id'],
        username=user_data['username'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
    )
    user.save()
    return user


class LoginView(APIView):
    def post(self, request):
        try:
            user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password'],
            )
        except ConnectionError:
            message = 'Сервер авторизации недоступен. Пожалуйста, попробуйте авторизоваться позднее'
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'non_field_errors': message})

        if not user:
            message = 'Неправильный пароль или пользователь не существует'
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'non_field_errors': message})

        login(request, user)
        return Response(status=status.HTTP_200_OK, data={})


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_307_TEMPORARY_REDIRECT, headers={'location': reverse('index')})


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            auth_user = microservice_auth_api.get_auth_user()
            user_data = auth_user.registrate(data['username'], data['password1'], data['email'])
            microservice_auth_api.save_auth_user(auth_user)
        except FieldsException as error:
            errors = error.errors
            if 'password' in errors:
                errors['password1'] = errors['password2'] = errors.pop('password')

            raise serializers.ValidationError(errors)

        if not user_data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={})
        elif 'microservice_auth_id' not in user_data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=user_data)

        user = create_user(
            microservice_auth_id=user_data['microservice_auth_id'],
            username=data['username'],
            first_name='',
            last_name='',
        )
        login(request, user)
        return Response(status=status.HTTP_200_OK, data={'success': True})


class ExternAuthGoogleView(APIView):
    def get(self, request):
        # Получаем токен от Google
        params = {
            'client_id': settings.EXTERN_AUTH['google']['client_id'],
            'client_secret': settings.EXTERN_AUTH['google']['client_secret'],
            'redirect_uri': '{}{}'.format(settings.SITE_URL, reverse('extern_auth_google')),
            'grant_type': 'authorization_code',
            'code': request.GET['code'],
        }
        response = requests.post('https://accounts.google.com/o/oauth2/token', params=params)
        data = response.json()
        access_token = data.get('access_token')
        if not access_token:
            context = {
                'success': False,
                'title': 'Ошибка авторизации через Google',
                'message': 'Неверный токен: {}, {}'.format(
                    data['error'],
                    data['error_description'],
                    ),
                
            }
            return render(request, 'base/message.html', context)

        # Авторизуемся через Google, получив в ответ данные пользователя

        if settings.MICROSERVICES_TOKENS.get('to_auth'):
            params = {
                'access_token': access_token,
                'id_token': data['id_token'],
                'token_type': 'Bearer',
                'expires_in': 3599,
            }
            response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', params=params)
            user_info = response.json()
            if not user_info['verified_email']:
                context = {'success': False, 'title': 'Ошибка авторизации через Google', 'message': 'E-mail в учётной записи Google не подтверждён. Пожалуйста, подтвердите e-mail и попробуйте авторизоваться вновь.'}
                return render(request, 'base/message.html', context)

            # создаём глобального и локального пользователя на Платформе

            user_data = microservice_auth_api.login_or_registrate_by_extern_service(
                username_for_new_user='{}-{}'.format(user_info['email'].split('@')[0], user_info['id'][-10:]),
                email=user_info['email'],
                first_name=user_info.get('given_name', ''),
                last_name=user_info.get('family_name', ''),
                extern_id='google-{}'.format(user_info['id']),
            )
            if not user_data:
                context = {
                    'success': False,
                    'title': 'Ошибка авторизации через Google',
                    'message': 'Не удалось авторизоваться через Google',
                }
                return render(request, 'base/message.html', context)
        else:
            try:
                auth_user = microservice_auth_api.get_auth_user()
                user_data = auth_user.login_or_registrate_by_extern(
                    'google',
                    access_token,
                    extra={'id_token': data['id_token']},
                )
                microservice_auth_api.save_auth_user(auth_user)
            except FieldsException as error:
                context = {
                    'success': False,
                    'title': 'Ошибка авторизации через Google',
                    'message': str(error.errors),
                }
                return render(request, 'base/message.html', context)

            # создаём глобального и локального пользователя на Платформе

        user = create_or_update_user(**user_data)
        login(request, user)
        context = {'success': True, 'title': 'Успешная авторизация через Google', 'message': 'Вы успешно авторизовались на сайте через Google. Теперь Вам доступны все возможности сервера'}
        return render(request, 'base/message.html', context)


class TokenView(LoginRequiredMixin, View):
    def get(self, request):
        tokens = Token.objects.filter(user=request.user).values('id', 'app_name')
        context = {'tokens': list(tokens)}
        return render(request, 'custom_auth/tokens.html', context=context)


class AddTokenView(LoginRequiredMixin, APIView):
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
        

class EditTokenView(LoginRequiredMixin, APIView):
    def post(self, request):
        serializer = EditTokenSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        token = Token.objects.get(user=request.user, pk=data['token_id'])
        token.app_name = data['app_name']
        token.save()
        data_for_response = {}
        return Response(status=status.HTTP_200_OK, data=data_for_response)


class DeleteTokenView(LoginRequiredMixin, APIView):
    def post(self, request, pk):
        token = Token.objects.get(user=request.user, pk=pk)
        token.delete()
        data_for_response = {}
        return Response(status=status.HTTP_200_OK, data=data_for_response)
