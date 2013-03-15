from misago.settings.settings import Settings

class SettingsMiddleware(object):
    def process_request(self, request):
        request.settings = Settings()
