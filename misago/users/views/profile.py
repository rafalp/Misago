from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render as django_render

from misago.core.shortcuts import get_object_or_404, paginate, validate_slug

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
        is_authenticated_user = context['profile'].pk == request.user.pk
    else:
        is_authenticated_user = False
    context['is_authenticated_user'] = is_authenticated_user

    user_acl = request.user.acl
    if request.user.is_authenticated():
        if is_authenticated_user:
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


@profile_view
def name_history(request, profile=None, page=0):
    name_changes_sq = profile.namechanges.all().order_by('-id')
    name_changes = paginate(name_changes_sq, page, 24, 6)
    items_left = name_changes.paginator.count - name_changes.end_index()

    return render(request, 'misago/profile/name_history.html', {
        'profile': profile,
        'name_changes': name_changes,
        'page_number': name_changes.number,
        'items_left': items_left
    })
