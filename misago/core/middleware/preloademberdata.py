class PreloadEmberDataMiddleware(object):
    def process_request(self, request):
        request.preloaded_ember_data = {}
