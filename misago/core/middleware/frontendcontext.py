class FrontendContextMiddleware(object):
    def process_request(self, request):
        request.frontend_context = {}
