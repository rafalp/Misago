from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

__all__ = ["authenticated_only", "anonymous_only"]


def authenticated_only(f):
    def perm_decorator(user_acl, target):
        if user_acl["is_anonymous"]:
            raise PermissionDenied(_("You have to sig in to perform this action."))
        return f(user_acl, target)

    return perm_decorator


def anonymous_only(f):
    def perm_decorator(user_acl, target):
        if user_acl["is_authenticated"]:
            raise PermissionDenied(_("Only guests can perform this action."))
        return f(user_acl, target)

    return perm_decorator
