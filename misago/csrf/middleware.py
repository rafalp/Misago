from misago.csrf import CSRFProtection
from misago.utils import get_random_string

class CSRFMiddleware(object):
    def process_request(self, request):
        if request.user.is_crawler():
            return None
        if 'csrf_token' in request.session:
            csrf_token = request.session['csrf_token']
        else:
            csrf_token = get_random_string(16);
            request.session['csrf_token'] = csrf_token
        request.csrf = CSRFProtection(csrf_token)