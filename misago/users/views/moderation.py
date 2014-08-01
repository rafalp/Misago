from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.core.decorators import require_POST
from misago.core.shortcuts import get_object_or_404, validate_slug

from misago.users.permissions.delete import allow_delete_user


def user_moderation_view(required_permission=None):
    def wrap(f):
        @transaction.atomic
        def decorator(request, *args, **kwargs):
            queryset = get_user_model().objects
            user_id = kwargs.pop('user_id')

            kwargs['user'] = get_object_or_404(queryset, id=user_id)
            validate_slug(kwargs['user'], kwargs.pop('user_slug'))
            add_acl(request.user, kwargs['user'])

            if required_permission:
                required_permission(request.user, kwargs['user'])

            return f(request, *args, **kwargs)
        return decorator
    return wrap


@require_POST
@user_moderation_view(allow_delete_user)
def delete(request, user):
    user.delete(delete_content=True)

    message = _("User %(username)s has been deleted.")
    messages.success(request, message % {'username': user.username})
    return redirect('misago:index')
