from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from .auth import (
    is_admin_authorized,
    remove_admin_authorization,
    update_admin_authorization,
)
from .views import get_protected_namespace
from .views.auth import login


class AdminAuthMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.admin_namespace = get_protected_namespace(request)
        if request.admin_namespace:
            return self.check_admin_authorization(request)

    def check_admin_authorization(self, request):
        if not is_admin_authorized(request):
            remove_admin_authorization(request)
            if request.resolver_match.url_name == "index":
                return login(request)
            return redirect("%s:index" % request.admin_namespace)

        update_admin_authorization(request)
