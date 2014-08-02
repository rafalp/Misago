from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import redirect, render as django_render

from misago.acl import add_acl
from misago.core.shortcuts import get_object_or_404, paginate, validate_slug

from misago.users import online
from misago.users.bans import get_user_ban
from misago.users.sites import user_profile


def profile_view(f):
    def decorator(request, *args, **kwargs):
        relations = ('rank', 'online_tracker', 'ban_cache')
        queryset = get_user_model().objects.select_related(*relations)
        profile = get_object_or_404(queryset, id=kwargs.pop('user_id'))

        validate_slug(profile, kwargs.pop('user_slug'))
        kwargs['profile'] = profile

        add_acl(request.user, profile)

        return f(request, *args, **kwargs)
    return decorator


def profile_view_restricted_visibility(f):
    @profile_view
    def decorator(request, *args, **kwargs):
        pages = user_profile.get_pages(request, kwargs['profile'])
        for page in pages:
            if page['is_active']:
                return f(request, *args, **kwargs)
        else:
            # we are trying to display page thats not in nav
            raise Http404()
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


@profile_view_restricted_visibility
def name_history(request, profile=None, page=0):
    name_changes_sq = profile.namechanges.all().order_by('-id')
    name_changes = paginate(name_changes_sq, page, 12, 4)
    items_left = name_changes.paginator.count - name_changes.end_index()

    return render(request, 'misago/profile/name_history.html', {
        'profile': profile,
        'name_changes': name_changes,
        'page_number': name_changes.number,
        'items_left': items_left
    })


@profile_view_restricted_visibility
def user_ban(request, profile=None):
    ban = get_user_ban(profile)
    if not ban:
        raise Http404()

    return render(request, 'misago/profile/ban_details.html', {
        'profile': profile,
        'ban': ban
    })
