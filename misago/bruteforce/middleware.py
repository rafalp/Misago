from misago.bruteforce.models import JamCache

class JamMiddleware(object):
    def process_request(self, request):
        if request.user.is_crawler():
            return None
        try:
            request.jam = request.session['jam']
        except KeyError:
            request.jam = JamCache()
            request.session['jam'] = request.jam
        if not request.firewall.admin:
            request.jam.check_for_updates(request)