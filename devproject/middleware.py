from time import time

from django.http import HttpRequest, HttpResponse


def time_middleware(get_response):
    def middleware(request: HttpRequest) -> HttpResponse:
        start_time = time()
        response = get_response(request)
        response.headers["Misago-Time"] = "{:.4f}s".format(time() - start_time)
        return response

    return middleware