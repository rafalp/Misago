from django.conf import settings
from django.http import HttpResponse

class HeartbeatMiddleware(object):
    def process_request(self, request):
        request.heartbeat = settings.HEARTBEAT_PATH and settings.HEARTBEAT_PATH == request.path
        if request.heartbeat:
            return HttpResponse('BATTLECRUISER OPERATIONAL')