from misago.dbsettings import DBSettings

class SettingsMiddleware(object):
    def process_request(self, request):
        request.settings = DBSettings()
