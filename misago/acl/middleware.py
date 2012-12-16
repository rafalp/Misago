from django.core.cache import cache, InvalidCacheBackendError
from misago.acl.builder import build_acl

class ACLMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            acl_key = request.user.make_acl_key()
        else:
            acl_key = request.session.get('acl_key')
            if not acl_key:
                acl_key = request.user.make_acl_key()
                request.session['acl_key'] = acl_key
        
        try:
            user_acl = cache.get(acl_key)
            if user_acl.version != request.monitor['acl_version']:
                raise InvalidCacheBackendError()
        except AttributeError, InvalidCacheBackendError:
            user_acl = build_acl(request, request.user.get_roles())
            cache.set(acl_key, user_acl, 2592000)
        
        request.acl = user_acl
        if request.user.is_authenticated() and (request.acl.team or request.user.is_god()) != request.user.is_team:
            request.user.is_team = (request.acl.team or request.user.is_god())
            request.user.save(force_update=True)
        request.session.team = request.user.is_team