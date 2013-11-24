from misago.utils.strings import random_string

class CSRFProtection(object):
    def __init__(self, csrf_token):
        self.csrf_id = '_csrf_token'
        self.csrf_token = csrf_token
        
    def request_secure(self, request):
        return request.method == 'POST' and request.POST.get(self.csrf_id) == self.csrf_token


class CSRFMiddleware(object):
    def process_request(self, request):
        if request.user.is_crawler():
            return None

        if 'csrf_token' in request.session:
            csrf_token = request.session['csrf_token']
        else:
            csrf_token = random_string(16);
            request.session['csrf_token'] = csrf_token
        
        request.csrf = CSRFProtection(csrf_token)
