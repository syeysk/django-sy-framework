from rest_framework import serializers


class AddTokenSerializer(serializers.Serializer):
    app_name = serializers.CharField(min_length=1, max_length=20)


class EditTokenSerializer(serializers.Serializer):
    app_name = serializers.CharField(min_length=1, max_length=20)
    token_id = serializers.IntegerField(min_value=1)
