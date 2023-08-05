from django.shortcuts import render
from rest_framework.views import APIView


class IntroView(APIView):
    def get(self, request):
        return render(request, 'pages/intro.html')


class MicroservicesListView(APIView):
    def get(self, request):
        return render(request, 'base/list_of_microservices.html')
