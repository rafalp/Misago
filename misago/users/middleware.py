from misago.users.models import AnonymousUser


class UserMiddleware(object):
    def process_request(self, request):
        if request.user.is_anonymous():
            request.user = AnonymousUser()
