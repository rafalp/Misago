from django.conf import settings
from misago.admin.auth import is_admin_session, update_admin_session
from misago.admin.views import get_protected_namespace
from misago.admin.views.auth import login


class AdminAuthMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.admin_namespace = get_protected_namespace(request)

        if request.admin_namespace:
            if not is_admin_session(request):
                return login(request)
            else:
                update_admin_session(request)
