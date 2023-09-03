from django_sy_framework.linker.models import Linker


def link_instances(link_to: str, link_to_id: int, instances: list['django.db.models.Model']):
    linkers = (Linker(link_to=link_to, link_to_id=link_to_id, content_object=instance) for instance in instances)
    Linker.objects.bulk_create(linkers, batch_size=100)


def link_instance_from_request(instance, request):
    link_to_parametr = request if isinstance(request, str) else request.GET.get('link_to')
    if link_to_parametr:
        link_to_parts = link_to_parametr.split('-')
        if len(link_to_parts) == 2:
            link_to, link_to_id = link_to_parts
            link_instances(link_to, int(link_to_id), [instance])
