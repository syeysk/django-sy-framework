from subprocess import check_output

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from syapi.exceptions import AccessDeniedException, FieldsException

from django_sy_framework.base.serializers import ProfileViewSerializer
from django_sy_framework.custom_auth.utils import microservice_auth_api


class IntroView(View):
    def get(self, request):
        return render(request, 'pages/intro.html')


class MicroservicesListView(View):
    def get(self, request):
        return render(request, 'base/list_of_microservices.html')


class RobotsTxtView(View):
    def get(self, _):
        content = 'User-agent: *\nAllow: /\nClean-param: s'
        return HttpResponse(content, content_type='text/plain')


class ProfileView(LoginRequiredMixin, APIView):
    def get(self, request):
        try:
            user_data = microservice_auth_api.get_auth_user(request.user.microservice_auth_id).get()
        except AccessDeniedException:
            logout(request)
            return redirect('custom_login_page')

        context = {'user_data': user_data}
        return render(request, 'base/profile.html', context)

    def post(self, request):
        serializer = ProfileViewSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        try:
            updated_fields = (
                microservice_auth_api.get_auth_user(user.microservice_auth_id).put(**data)['updated_fields']
            )
        except FieldsException as error:
            raise serializers.ValidationError(error.errors)

        if 'first_name' in updated_fields:
            user.first_name = data['first_name']

        if 'last_name' in updated_fields:
            user.last_name = data['last_name']

        if 'username' in updated_fields:
            user.username = data['username']

        if updated_fields:
            user.save()

        result_data = {'updated': updated_fields}
        return Response(status=status.HTTP_200_OK, data=result_data)

    def delete(self, request):
        user = request.user
        success = microservice_auth_api.get_auth_user(user.microservice_auth_id).delete()
        if not success:
            return Response(status=status.HTTP_201_CREATED, data={'success': False})

        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceServerView(LoginRequiredMixin, APIView):
    def get(self, request):
        return render(request, 'base/service_server.html')

    def post(self, request):
        command = request.POST.get('command')
        message = None
        if command == 'deploy_server':
            message = check_output('cd .. ; git pull origin main', shell=True)
        elif command == 'restart_server':
            check_output('touch tmp/restart.txt', shell=True)
        else:
            message = 'unknown command'

        data = {'message': message}
        return Response(status=status.HTTP_200_OK, data=data)
