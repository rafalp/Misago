from django.conf import settings
from misago.admin.auth import is_admin_session
from misago.admin.views import get_admin_namespace
from misago.admin.views.auth import login


class AdminAuthMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.admin_namespace = get_admin_namespace(
            request.resolver_match.namespace)

        if request.admin_namespace and not is_admin_session(request):
            return login(request)
