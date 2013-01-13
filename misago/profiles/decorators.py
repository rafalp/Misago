from functools import wraps
from misago.utils import slugify
from misago.views import error404
from misago.users.models import User

def profile_view(fallback='user'):
    def outer_decorator(f):
        def inner_decorator(request, user, username, *args, **kwargs):
            request = request
            user_pk = int(user)
            user_slug = username
            try:
                user = User.objects.get(pk=user_pk)
                if user.username_slug != user_slug:
                    # Force crawlers to take notice of updated username
                    return redirect(reverse(fallback, args=(user.username_slug, user.pk)), permanent=True)
                return f(request, user, *args, **kwargs)
            except User.DoesNotExist:
                return error404(request)
    
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