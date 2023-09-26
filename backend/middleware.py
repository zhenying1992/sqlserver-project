import logging

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class ErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logging.error(exception, exc_info=True)
        return JsonResponse(str(exception), status=400, safe=False)
