from time import time

from django.http import HttpRequest, HttpResponse


def view_time_middleware(get_response):
    def middleware(request: HttpRequest) -> HttpResponse:
        start_time = time()
        response = get_response(request)
        response.headers["Misago-View-Time"] = "{:.4f}s".format(time() - start_time)
        return response

    return middleware


def response_time_middleware(get_response):
    def middleware(request: HttpRequest) -> HttpResponse:
        start_time = time()
        response = get_response(request)
        response.headers["Misago-Response-Time"] = "{:.4f}s".format(time() - start_time)
        return response

    return middleware
