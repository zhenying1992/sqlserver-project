from django.shortcuts import render

from django.http import JsonResponse
from django.contrib.auth import authenticate

user = authenticate(username='john', password='secret')


def loginView(request):
    print(request.body, request.POST)
    print(dir(request))
    return JsonResponse({'status': 1})
