from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render as django_render

from misago.core.shortcuts import get_object_or_404, validate_slug

from misago.users import online
from misago.users.sites import user_profile


def profile_view(f):
    def decorator(*args, **kwargs):
        relations = ('rank', 'online_tracker', 'ban_cache')
        queryset = get_user_model().objects.select_related(*relations)
        profile = get_object_or_404(queryset, id=kwargs.pop('user_id'))

        validate_slug(profile, kwargs.pop('user_slug'))
        kwargs['profile'] = profile

        return f(*args, **kwargs)
    return decorator


def render(request, template, context):
    context['pages'] = user_profile.get_pages(request, context['profile'])
    for page in context['pages']:
        if page['is_active']:
            context['active_page'] = page
            break

    if request.user.is_authenticated():
        authenticateds_profile = context['profile'].pk == request.user.pk
    else:
        authenticateds_profile = False
    context['authenticateds_profile'] = authenticateds_profile

    user_acl = request.user.acl
    if request.user.is_authenticated():
        if authenticateds_profile:
            context['show_email'] = True
        else:
            context['show_email'] = user_acl['can_see_users_emails']
    else:
        context['show_email'] = False

    context['state'] = online.state_for_acl(context['profile'], user_acl)

    return django_render(request, template, context)


@profile_view
def user_posts(request, profile=None, page=0):
    return render(request, 'misago/profile/posts.html', {'profile': profile})


@profile_view
def user_threads(request, profile=None, page=0):
    return render(request, 'misago/profile/threads.html', {'profile': profile})
