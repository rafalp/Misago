from misago.monitor.monitor import Monitor

class MonitorMiddleware(object):
    def process_request(self, request):
        request.monitor = Monitor()