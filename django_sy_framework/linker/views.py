from itertools import chain

from django.core.paginator import Paginator
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django_sy_framework.linker.models import Linker
from django_sy_framework.linker.serializers import LinkerGetViewSerializer, LinkerPutViewSerializer
from django_sy_framework.linker.utils import link_instances
from django_sy_framework.utils.authentication import AnonymousTokenAuthentication
from django_sy_framework.utils.permissions import IsRequestFromMicroservice


class LinkerView(APIView):
    authentication_classes = [AnonymousTokenAuthentication]
    permission_classes = [IsRequestFromMicroservice]

    @extend_schema(
        tags=['Привязка объектов'],
        parameters=[
        ],
        request=LinkerGetViewSerializer,
        responses={},
        description='Получает привязанные объекты',
        summary='Получить привязанные объекты',
    )
    def post(self, request, link_to: str, link_to_id: int):
        serializer = LinkerGetViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        related_name = data['object']
        queryset = (
            Linker.objects
            .filter(
                link_to=link_to,
                link_to_id=link_to_id,
                **{f'{related_name}__isnull': False},
            )
        )

        order_by = [
            '{}{}__{}'.format(
                '-' if field.startswith('-') else '',
                related_name,
                field[1:] if field.startswith('-') else field,
            )
            for field in data['order_by']
        ]
        objects = queryset.order_by(*order_by)
        paginator = Paginator(objects, data['on_page'])
        page = paginator.page(data['p'])

        fields = [f'{related_name}__{field}' for field in data['fields']]
        linked_objects = []
        for linker in page.object_list.only(*fields):
            linked_object = {
                field: getattr(linker.content_object, field) for field in chain(data['fields'], data['extra_fields'])
            }
            linked_objects.append(linked_object)

        linked_model = getattr(Linker, data['object']).rel.related_model
        response_data = {
            'objects': linked_objects,
            'page': data['p'],
            'num_pages': paginator.num_pages,
            'url_new': linked_model().url_new,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)

    @extend_schema(
        tags=['Привязка объектов'],
        parameters=[
        ],
        request=LinkerPutViewSerializer,
        responses={202: None},
        description='Привязывает несколько объектов к другому (например, несколько заметок к проекту)',
        summary='Привязать объекты',
    )
    def put(self, request, link_to: str, link_to_id: int):
        serializer = LinkerPutViewSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        querysets = []
        for linker in serializer.validated_data:
            linked_model = getattr(Linker, linker['object']).rel.related_model
            querysets.append(linked_model.objects.filter(pk__in=linker['object_ids']).only('pk'))

        if querysets:
            link_instances(link_to, link_to_id, chain(*querysets))

        return Response(status=status.HTTP_202_ACCEPTED)
