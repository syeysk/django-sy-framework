from rest_framework import serializers


class LinkerGetViewSerializer(serializers.Serializer):
    object = serializers.CharField(help_text='Тип привязанного объекта', max_length=10)
    p = serializers.IntegerField(
        help_text='Номер страницы',
        min_value=1,
        default=1,
    )
    on_page = serializers.IntegerField(
        help_text='Количество объектов на странице',
        min_value=1,
        default=10,
    )
    order_by = serializers.ListSerializer(
        help_text='Поля, по которым нужно отсортировать объекты',
        child=serializers.CharField(
            help_text='Имя поля, по которому нужно отсортировать объекты',
            min_length=1,
            max_length=50,
        ),
        allow_null=False,
        default=list(['-id']),
    )
    fields = serializers.ListSerializer(
        help_text='Возвращаемые поля',
        child=serializers.CharField(
            help_text='Имя возвращаемого поля',
            min_length=1,
            max_length=50,
        ),
        allow_null=False,
        default=list(['-pk']),
    )
    extra_fields = serializers.ListSerializer(
        help_text='Возвращаемые поля (на уровне Питона, а не базы)',
        child=serializers.CharField(
            help_text='Имя возвращаемого поля',
            min_length=1,
            max_length=50,
        ),
        allow_null=False,
        default=list(),
    )


class LinkerPutViewSerializer(serializers.Serializer):
    object = serializers.CharField(help_text='Тип привязываемого объекта', max_length=10)
    object_ids = serializers.ListField(
        help_text='Список идентификаторов привязываемых объектов',
        child=serializers.IntegerField(help_text='Идентификаторов привязываемого объекта', min_value=1),
        allow_null=False,
        default=list([]),
    )
