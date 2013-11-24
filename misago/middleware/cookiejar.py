from misago.cookiejar import CookieJar

class CookieJarMiddleware(object):
    def process_request(self, request):
        request.cookiejar = CookieJar()

    def process_response(self, request, response):
        try:
            request.cookiejar.flush(response)
        except AttributeError:
            pass
        return response
