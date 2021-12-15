from django.http import JsonResponse
from finance.views.base import login_require
from finance.utils import list_local_cpu, list_local_disk, get_local_memory
from dataclasses import asdict


@login_require
def cpuView(request):
    return JsonResponse(
        {
            'status': 'success',
            'data': [asdict(cpu) for cpu in list_local_cpu()]
        }
    )


@login_require
def memoryView(request):
    return JsonResponse(
        {
            'status': 'success',
            'data': asdict(get_local_memory())
        }
    )


@login_require
def diskView(request):
    return JsonResponse(
        {
            'status': 'success',
            'data': [asdict(disk) for disk in list_local_disk()]
        }
    )
