from django.utils.deprecation import MiddlewareMixin

from .. import threadstore


class ThreadStoreMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        threadstore.clear()
        return response
