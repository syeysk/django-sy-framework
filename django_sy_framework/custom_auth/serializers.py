from re import search
from rest_framework import serializers


class RegistrationSerializer(serializers.Serializer):
    PASSWORD_VALIDATION_ERROR = (
        'Пароль должен содержать следующие группы символов: цифры, заглавные и строчные буквы и спецсимволы _/-'
    )

    def validate_password1(self, value):
        for template in ('[0-9]', '[a-z]', '[A-Z]', '[_-]'):
            if not search(template, value):
                raise serializers.ValidationError(self.PASSWORD_VALIDATION_ERROR)

        return value

    def validate_password2(self, value):
        return self.validate_password1(value)

    def validate_data(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Пароли должны совпадать')

        return data

    password1 = serializers.CharField(min_length=10, max_length=50)
    password2 = serializers.CharField(min_length=10, max_length=50)
    username = serializers.SlugField(min_length=1, max_length=50)
    email = serializers.EmailField(min_length=3, max_length=50)
