from re import match
from rest_framework import serializers


class RegistrationSerializer(serializers.Serializer):
    PASSWORD_VALIDATION_ERROR = (
        'Пароль должен содержать следующие группы символов: цифры, заглавные и строчные буквы и спецсимволы _/-'
    )

    def validate_password1(self, value):
        for template in ('[0-9]', '[a-z]', '[A-Z]', '[_-]'):
            if not match(template, value):
                raise serializers.ValidationError(self.PASSWORD_VALIDATION_ERROR)

        return value

    def validate_data(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Пароли должны совпадать')

        return data


    password1 = serializers.CharField(min_length=10, max_length=50)
    password2 = serializers.CharField(min_length=10, max_length=50)
    username = serializers.SlugField(min_length=1, max_length=50)
    email = serializers.EmailField(min_length=3, max_length=50)


class AddTokenSerializer(serializers.Serializer):
    app_name = serializers.CharField(min_length=1, max_length=20)


class EditTokenSerializer(serializers.Serializer):
    app_name = serializers.CharField(min_length=1, max_length=20)
    token_id = serializers.IntegerField(min_value=1)
