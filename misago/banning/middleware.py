from misago.banning.models import BanCache
from misago.users.models import Guest

class BanningMiddleware(object):
    def process_request(self, request):
        if request.user.is_crawler():
            return None
        try:
            request.ban = request.session['ban']
        except KeyError:
            request.ban = BanCache()
            request.session['ban'] = request.ban
        if not request.firewall.admin:
            request.ban.check_for_updates(request)
            # Make sure banned session is downgraded to guest level
            if request.ban.is_banned():
                request.session.sign_out(request)