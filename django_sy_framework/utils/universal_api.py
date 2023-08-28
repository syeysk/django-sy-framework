import requests
from django.conf import settings


class MethodAPI:
    def __init__(self, api_version, microservice_name, api_method):
        self.microservice_name = microservice_name
        self.api_version = api_version
        self.api_method = api_method

    def __getattr__(self, method_str):
        token = settings.MICROSERVICES_TOKENS[f'to_{self.microservice_name}']
        microservice_url = settings.MICROSERVICES_URLS[self.microservice_name]
        url = f'{microservice_url}/api/v{self.api_version}/{self.microservice_name}/{self.api_method}'
        http_method = getattr(requests, method_str)

        def get_request_func(path, **kwargs):
            headers = kwargs.setdefault('headers', {})
            headers['AUTHORIZATION'] = f'Token {token}'
            return http_method(f'{url}{path}', **kwargs)

        return get_request_func


class MicroserviceAPI:
    def __init__(self, api_version, microservice_name):
        self.microservice_name = microservice_name
        self.api_version = api_version

    def __getattr__(self, api_method):
        return MethodAPI(self.api_version, self.microservice_name, api_method)


class API:
    def __init__(self, api_version):
        self.api_version = api_version

    def __getattr__(self, microservice_name):
        return MicroserviceAPI(self.api_version, microservice_name)
