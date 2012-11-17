from . import Stopwatch

class StopwatchMiddleware(object):
    def process_request(self, request):
        request.stopwatch = Stopwatch()
        
    def process_response(self, request, response):
        try:
            time = request.stopwatch.time()
            import os
            stat_file = open(os.getcwd() + os.sep + 'stopwatch.txt', 'a')
            stat_file.write("%s s\n" % time)
            stat_file.close()
        except AttributeError:
            pass
        return response