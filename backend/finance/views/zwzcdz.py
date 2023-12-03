import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from finance.models import Zwzcdz
from django.core.paginator import Paginator


def ZwzcdzView(request):
    data = json.loads(request.body.decode("utf8"))
    q = Zwzcdz.objects

    if 'kjnd' in data:
        q = q.filter(kjnd=data['kjnd'])

    if 'kjqj' in data:
        q = q.filter(kjqj=data['kjqj'])

    if 'zy' in data:
        q = q.filter(zy__contains=data['zy'])

    if 'dje' in data:
        q = q.fitler(dje=data['dje'])

    current = data['current'] if 'current' in data else 1
    page_size = data['pageSize'] if 'pageSize' in data else 2
    pagination = Paginator(q.all(), page_size)
    page = pagination.page(current)
    objs = [model_to_dict(obj) for obj in page.object_list]
    data = {
        "current": page.number,
        "pageSize": page_size,
        "count": pagination.count,
        "size": pagination.num_pages,
        "data": objs,
    }
    return JsonResponse(data={'data': data, 'status': True})
