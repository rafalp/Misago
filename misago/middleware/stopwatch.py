from django.conf import settings
from misago.core.stopwatch import Stopwatch

class StopwatchMiddleware(object):
    def process_request(self, request):
        request.stopwatch = Stopwatch()

    def process_response(self, request, response):
        try:
            if settings.STOPWATCH_LOG:
                stat_file = open(settings.STOPWATCH_LOG, 'a')
                stat_file.write("%s %s s\n" % (request.path_info, request.stopwatch.time()))
                stat_file.close()
        except AttributeError:
            pass
        return response
