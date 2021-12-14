from django.http import JsonResponse
from finance.views.base import login_require
from finance.utils import get_disk

@login_require
def cpuView(request):
    return JsonResponse({'data': TASK_LIST})

def diskView(request):
    return JsonResponse({'data': get_disk(), 'status': "success"})

@login_require
def memoryView(request):
    return