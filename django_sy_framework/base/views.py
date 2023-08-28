from subprocess import check_output

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_sy_framework.base.serializers import ProfileViewSerializer
from django_sy_framework.custom_auth.utils import microservice_auth_api


class IntroView(APIView):
    def get(self, request):
        return render(request, 'pages/intro.html')


class MicroservicesListView(APIView):
    def get(self, request):
        return render(request, 'base/list_of_microservices.html')


class ProfileView(LoginRequiredMixin, APIView):
    def get(self, request):
        user_data = microservice_auth_api.get(username=request.user.username)
        context = {'user_data': user_data}
        return render(request, 'base/profile.html', context)

    def post(self, request):
        serializer = ProfileViewSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        updated_fields = microservice_auth_api.edit(current_username=user.username, **data)

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
