from misago.acl.builder import acl

class ACLMiddleware(object):
    def process_request(self, request):
        request.acl = acl(request.user)

        if (request.user.is_authenticated() and
            (request.acl.team or request.user.is_god()) != request.user.is_team):
            request.user.is_team = (request.acl.team or request.user.is_god())
            request.user.save(force_update=True)

        if request.session.team != request.user.is_team:
            request.session.team = request.user.is_team
            request.session.save()
