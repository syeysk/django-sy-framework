from subprocess import check_output

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProfileViewSerializer


class IntroView(APIView):
    def get(self, request):
        return render(request, 'pages/intro.html')


class MicroservicesListView(APIView):
    def get(self, request):
        return render(request, 'base/list_of_microservices.html')


class ProfileView(LoginRequiredMixin, APIView):
    def get(self, request):
        context = {}
        return render(request, 'base/profile.html', context)

    def post(self, request):
        serializer = ProfileViewSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        update_fields = []
        if user.first_name != data['first_name']:
            user.first_name = data['first_name']
            update_fields.append('first_name')

        if user.last_name != data['last_name']:
            user.last_name = data['last_name']
            update_fields.append('last_name')

        if update_fields:
            user.save()

        result_data = {'success': True, 'updated': update_fields}
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
