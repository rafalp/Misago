from django.utils import timezone
from misago.sessions import CrawlerSession, HumanSession

class SessionMiddleware(object):
    def process_request(self, request):
        try:
            if request.user.is_crawler():
                # Crawler Session
                request.session = CrawlerSession(request)
        except AttributeError:
            # Human Session
            request.session = HumanSession(request)
            request.user = request.session.get_user()

            if request.user.is_authenticated():
                request.session.set_hidden(request.user.hide_activity > 0)

    def process_response(self, request, response):
        try:
            # Sync last visit date
            if request.user.is_authenticated():
                visit_sync = request.session.get('visit_sync')
                if not visit_sync or (timezone.now() - visit_sync).seconds >= 900:
                    request.session['visit_sync'] = timezone.now()
                    request.user.last_date = timezone.now()
                    request.user.save(force_update=True)
            request.session.save()
        except AttributeError:
            pass
        return response
