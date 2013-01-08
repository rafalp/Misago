from misago.cookie_jar.cookie_jar import CookieJar

class CookieJarMiddleware(object):
    def process_request(self, request):
        request.cookie_jar = CookieJar()

    def process_response(self, request, response):
        try:
            request.cookie_jar.flush(response)
        except AttributeError:
            pass
        return response
