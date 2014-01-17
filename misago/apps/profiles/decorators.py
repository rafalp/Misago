from functools import wraps
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.models import User
from misago.utils.strings import slugify

def profile_view(fallback='user'):
    def outer_decorator(f):
        def inner_decorator(request, user, username, *args, **kwargs):
            request = request
            user_pk = int(user)
            user_slug = username
            try:
                user = User.objects
                if settings.PROFILE_EXTENSIONS_PRELOAD:
                    user = user.select_related(*settings.PROFILE_EXTENSIONS_PRELOAD)
                user = user.get(pk=user_pk)
                if user.username_slug != user_slug:
                    # Force crawlers to take notice of updated username
                    return redirect(reverse(fallback, args=(user.username_slug, user.pk)), permanent=True)
                return f(request, user, *args, **kwargs)
            except User.DoesNotExist:
                return error404(request)
            except ACLError404:
                return error404(request)
            except ACLError403 as e:
                return error403(request, e.message)
        return wraps(f)(inner_decorator)
    return outer_decorator


def user_view(f):
    def inner_decorator(request, user, *args, **kwargs):
        request = request
        user_pk = int(user)
        try:
            user = User.objects.get(pk=user_pk)
            return f(request, user, *args, **kwargs)
        except User.DoesNotExist:
            return error404(request)

    return wraps(f)(inner_decorator)