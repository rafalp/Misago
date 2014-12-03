from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.transaction import atomic
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render as django_render
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.core.decorators import require_POST
from misago.core.shortcuts import get_object_or_404, paginate, validate_slug
from misago.core.utils import clean_return_path
from misago.notifications import notify_user, read_user_notification
from misago.threads.permissions import allow_message_user

from misago.users.bans import get_user_ban
from misago.users.decorators import deny_guests
from misago.users.online.utils import get_user_state
from misago.users.permissions.profiles import (allow_follow_user,
                                               allow_block_user)
from misago.users.sites import user_profile
from misago.users.warnings import (get_warning_levels, get_user_warning_level,
                                   get_user_warning_obj)


def profile_view(f):
    def decorator(request, *args, **kwargs):
        User = get_user_model()

        relations = ('rank', 'online_tracker', 'ban_cache')
        queryset = User.objects.select_related(*relations)
        profile = get_object_or_404(queryset, id=kwargs.pop('user_id'))

        validate_slug(profile, kwargs.pop('user_slug'))
        kwargs['profile'] = profile

        add_acl(request.user, profile)

        if profile.acl_['can_follow']:
            profile.is_followed = request.user.is_following(profile)
        else:
            profile.is_followed = False

        if profile.acl_['can_block'] and request.user.is_authenticated():
            profile.is_blocked = request.user.is_blocking(profile)
        else:
            profile.is_blocked = False

        if request.user.is_authenticated and request.method == "GET":
            read_user_notification(request.user, "profile_%s" % profile.pk)

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


def notification_view(trigger):
    def function_decorator(f):
        def decorator(*args, **kwargs):
            request = args[0]
            user = request.user
            profile = kwargs.get('profile')

            if user.is_authenticated and request.method == "GET":
                read_user_notification(user, trigger % profile.pk)

            return f(*args, **kwargs)
        return decorator
    return function_decorator


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

    context['state'] = get_user_state(context['profile'], user_acl)

    if request.user.is_authenticated():
        try:
            allow_message_user(request.user, context['profile'])
            context['can_message'] = True
        except PermissionDenied as e:
            context['can_message'] = False
            context['cant_message_reason'] = e

    return django_render(request, template, context)


@profile_view
def posts(request, profile, page=0):
    return render(request, 'misago/profile/posts.html', {'profile': profile})


@profile_view
def threads(request, profile, page=0):
    return render(request, 'misago/profile/threads.html', {'profile': profile})


@profile_view
def followers(request, profile, page=0):
    followers_qs = profile.followed_by.order_by('slug')
    followers = paginate(followers_qs, page, 6 * 4, 6)
    items_left = followers.paginator.count - followers.end_index()

    if followers.paginator.count != profile.followers:
        profile.followers = followers.paginator.count
        profile.save(update_fields=['followers'])

    return render(request, 'misago/profile/followers.html', {
        'profile': profile,
        'followers': followers,
        'items_left': items_left,
    })


@profile_view
def follows(request, profile, page=0):
    followers_qs = profile.follows.order_by('slug')
    followers = paginate(followers_qs, page, 6 * 4, 6)
    items_left = followers.paginator.count - followers.end_index()

    if followers.paginator.count != profile.following:
        profile.following = followers.paginator.count
        profile.save(update_fields=['following'])

    return render(request, 'misago/profile/follows.html', {
        'profile': profile,
        'followers': followers,
        'items_left': items_left,
    })


@profile_view_restricted_visibility
@notification_view("warnings_%s")
def warnings(request, profile, page=0):
    warnings_qs = profile.warnings.order_by('-id')
    warnings = paginate(warnings_qs, page, 5, 2)
    items_left = warnings.paginator.count - warnings.end_index()

    add_acl(request.user, warnings.object_list)

    warning_level = get_user_warning_level(profile)
    warning_level_obj = get_user_warning_obj(profile)

    active_warnings = warning_level - warnings.start_index() + 1
    for warning in warnings.object_list:
        if warning.is_canceled:
            warning.is_active = False
        else:
            warning.is_active = active_warnings > 0
            active_warnings -= 1

    levels_total = len(get_warning_levels()) - 1
    if levels_total and warning_level:
        warning_progress = 100 - warning_level * 100 / levels_total
    else:
        warning_progress = 100

    if warning_level:
        warning_level_obj.level = warning_level

    return render(request, 'misago/profile/warnings.html', {
        'profile': profile,
        'warnings': warnings,
        'warning_level': warning_level_obj,
        'warning_progress': warning_progress,
        'page_number': warnings.number,
        'items_left': items_left
    })


@profile_view_restricted_visibility
@notification_view("name_history_%s")
def name_history(request, profile, page=0):
    name_changes_qs = profile.namechanges.all().order_by('-id')
    name_changes = paginate(name_changes_qs, page, 12, 4)
    items_left = name_changes.paginator.count - name_changes.end_index()

    return render(request, 'misago/profile/name_history.html', {
        'profile': profile,
        'name_changes': name_changes,
        'page_number': name_changes.number,
        'items_left': items_left
    })


@profile_view_restricted_visibility
def user_ban(request, profile):
    ban = get_user_ban(profile)
    if not ban:
        raise Http404()

    return render(request, 'misago/profile/ban_details.html', {
        'profile': profile,
        'ban': ban
    })


"""
Profile actions
"""
def action_view(f):
    @deny_guests
    @require_POST
    @profile_view
    @atomic
    def decorator(request, profile):
        response = f(request, profile.lock())
        if request.is_ajax():
            response['is_error'] = False
            return JsonResponse(response)
        else:
            messages.success(request, response['message'])
            return_path = clean_return_path(request)
            if return_path:
                return redirect(return_path)
            else:
                return redirect(user_profile.get_default_link(),
                                user_slug=profile.slug, user_id=profile.id)
    return decorator


@action_view
def follow_user(request, profile):
    user_locked = request.user.lock()
    profile.lock()

    if request.user.is_following(profile):
        request.user.follows.remove(profile)
        followed = False
    else:
        allow_follow_user(request.user, profile)
        followed = True
        request.user.follows.add(profile)

    if followed:
        message = _("You are now following %(user)s.")
        notify_user(profile,
            _("%(user)s is now following you."),
            reverse(user_profile.get_default_link(), kwargs={
                'user_slug': user_locked.slug, 'user_id': user_locked.id
            }),
            "profile_%s" % user_locked.pk,
            formats={'user': user_locked.username},
            sender=user_locked,
            update_user=False)
    else:
        message = _("You have stopped following %(user)s.")
    message = message % {'user': profile.username}

    profile.followers = profile.followed_by.count()
    if followed:
        profile.save(update_fields=['followers', 'new_notifications'])
    else:
        profile.save(update_fields=['followers'])

    user_locked.following = user_locked.follows.count()
    user_locked.save(update_fields=['following'])

    if request.is_ajax:
        return {'is_following': followed, 'message': message}
    else:
        messages.success(request, message)


@action_view
def block_user(request, profile):
    request.user.lock()

    if request.user.is_blocking(profile):
        request.user.blocks.remove(profile)
        blocked = False
    else:
        allow_block_user(request.user, profile)
        blocked = True
        request.user.blocks.add(profile)

    if blocked:
        message = _("You are now blocking %(user)s.")
    else:
        message = _("You have stopped blocking %(user)s.")
    message = message % {'user': profile.username}

    if request.is_ajax:
        return {'is_blocking': blocked, 'message': message}
    else:
        messages.success(request, message)
