from sessions import SessionCrawler, SessionHuman

class SessionMiddleware(object):
    def process_request(self, request):
        try:
            if request.user.is_crawler():
                # Crawler Session
                request.session = SessionCrawler(request)
        except AttributeError:
            # Human Session
            request.session = SessionHuman(request)
            request.user = request.session.get_user()
            
            if request.settings['sessions_hidden'] and request.user.is_authenticated():
                request.session.set_hidden(request.user.hide_activity > 0)
                    
    def process_response(self, request, response):
        try:
            request.session.save(request, response)
        except AttributeError:
            pass
        return response