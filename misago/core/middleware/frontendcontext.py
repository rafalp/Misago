class FrontendContextMiddleware(object):
    def process_request(self, request):
        request.include_frontend_context = True
        request.frontend_context = {}
