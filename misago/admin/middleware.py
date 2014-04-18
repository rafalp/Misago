from django.conf import settings
from misago.admin.auth import is_admin_session
from misago.admin.views.auth import login


class AdminAuthMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        url_namespace = request.resolver_match.namespace
        admin_request = url_namespace in settings.MISAGO_ADMIN_NAMESPACES
        request.misago_admin_auth = admin_request

        if request.misago_admin_auth and not is_admin_session(request):
            return login(request)
