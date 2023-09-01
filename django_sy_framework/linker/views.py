from itertools import chain

from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django_sy_framework.linker.models import Linker
from django_sy_framework.linker.serializers import LinkerGetViewSerializer, LinkerPutViewSerializer


class LinkerView(APIView):
    def post(self, request, link_to: str, link_to_id: str):
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

        objects = queryset.order_by(*data['order_by'])
        paginator = Paginator(objects, data['on_page'])
        page = paginator.page(data['p'])

        fields = [f'{related_name}__{field}' for field in data['fields']]
        linked_objects = []
        for linker in page.object_list.only(*fields):
            linked_object = {
                field: getattr(linker.content_object, field) for field in chain(data['fields'], data['extra_fields'])
            }
            linked_objects.append(linked_object)

        response_data = {
            'objects': linked_objects,
            'page': data['p'],
            'num_pages': paginator.num_pages,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)

    def put(self, request, link_to: str, link_to_id: str):
        serializer = LinkerPutViewSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        linkers = []
        for linker in serializer.validated_data:
            linked_model = getattr(Linker, linker['object']).rel.related_model
            linked_objects = linked_model.objects.filter(pk__in=linker['object_ids']).only('pk')
            for linked_object in linked_objects:
                linkers.append(
                    Linker(link_to=link_to, link_to_id=link_to_id, content_object=linked_object),
                )

        Linker.objects.bulk_create(linkers, batch_size=100)
        return Response(status=status.HTTP_202_ACCEPTED)

    def delete(self, request, link_to: str, link_to_id: str):
        ...
