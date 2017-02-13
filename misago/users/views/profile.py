from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic
from django.http import Http404, JsonResponse
from django.shortcuts import render as django_render
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import six
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.conf import settings
from misago.core.decorators import require_POST
from misago.core.shortcuts import get_object_or_404, paginate, pagination_dict, validate_slug
from misago.core.utils import clean_return_path
from misago.threads.permissions import allow_message_user
from misago.users.bans import get_user_ban
from misago.users.decorators import deny_guests
from misago.users.online.utils import get_user_status
from misago.users.pages import user_profile
from misago.users.permissions.profiles import allow_block_user, allow_follow_user
from misago.users.serializers import BanDetailsSerializer, UserSerializer, UserCardSerializer
from misago.users.serializers.usernamechange import UsernameChangeSerializer
from misago.users.viewmodels import UserPosts, UserThreads


UserModel = get_user_model()


def profile_view(f):
    def decorator(request, *args, **kwargs):
        relations = ('rank', 'online_tracker', 'ban_cache')
        queryset = UserModel.objects.select_related(*relations)

        profile = get_object_or_404(queryset, pk=kwargs.pop('pk'))

        if not profile.is_active and not request.user.is_staff:
            raise Http404()

        validate_slug(profile, kwargs.pop('slug'))
        kwargs['profile'] = profile

        add_acl(request.user, profile)

        return f(request, *args, **kwargs)
    return decorator


def profile_view_restricted_visibility(f):
    @profile_view
    def decorator(request, *args, **kwargs):
        sections = user_profile.get_sections(request, kwargs['profile'])
        for section in sections:
            if section['is_active']:
                return f(request, *args, **kwargs)
        else:
            # we are trying to display page thats not in nav
            raise Http404()
    return decorator


def render(request, template, context):
    request.frontend_context['PROFILE_PAGES'] = []

    context['sections'] = user_profile.get_sections(request, context['profile'])

    for section in context['sections']:
        request.frontend_context['PROFILE_PAGES'].append({
            'name': six.text_type(section['name']),
            'icon': section['icon'],
            'meta': section.get('metadata'),
            'component': section['component'],
        })

        if section['is_active']:
            context['active_section'] = section

    if request.user.is_authenticated:
        is_authenticated_user = context['profile'].pk == request.user.pk
    else:
        is_authenticated_user = False
    context['is_authenticated_user'] = is_authenticated_user

    if request.user.is_authenticated:
        if is_authenticated_user:
            context['show_email'] = True
        else:
            context['show_email'] = request.user.acl['can_see_users_emails']
    else:
        context['show_email'] = False

    context['profile'].status = get_user_status(request.user, context['profile'])

    request.frontend_context['PROFILE'] = UserProfileSerializer(
        context['profile'], context={'user': request.user}).data

    if not context['profile'].is_active:
        request.frontend_context['PROFILE']['is_active'] = False

    return django_render(request, template, context)


@profile_view
def landing(request, profile):
    return redirect(user_profile.get_default_link(), slug=profile.slug, pk=profile.pk)


@profile_view
def posts(request, profile):
    context = {
        'profile': profile,
    }

    feed = UserPosts(request, profile)
    context.update(feed.get_template_context())

    request.frontend_context['POSTS'] = feed.get_frontend_context()

    return render(request, 'misago/profile/posts.html', context)


@profile_view
def threads(request, profile):
    context = {
        'profile': profile
    }

    feed = UserThreads(request, profile)
    context.update(feed.get_template_context())

    request.frontend_context['POSTS'] = feed.get_frontend_context()

    return render(request, 'misago/profile/threads.html', context)


@profile_view
def followers(request, profile):
    queryset = profile.followed_by.select_related('rank').order_by('slug')

    page = paginate(queryset, None, 12, 4)
    paginator = pagination_dict(page)

    request.frontend_context['PROFILE_FOLLOWERS'] = dict(
        results=UserCardSerializer(page.object_list, many=True).data,
        **paginator
    )

    return render(request, 'misago/profile/followers.html', {
        'profile': profile,
        'followers': page.object_list,
        'count': paginator['count'],
    })


@profile_view
def follows(request, profile):
    queryset = profile.follows.select_related('rank').order_by('slug')

    page = paginate(queryset, None, settings.MISAGO_USERS_PER_PAGE, 4)
    paginator = pagination_dict(page)

    request.frontend_context['PROFILE_FOLLOWS'] = dict(
        results=UserCardSerializer(page.object_list, many=True).data,
        **paginator
    )

    return render(request, 'misago/profile/follows.html', {
        'profile': profile,
        'follows': page.object_list,
        'count': paginator['count'],
    })


@profile_view_restricted_visibility
def username_history(request, profile):
    queryset = profile.namechanges.select_related('user', 'changed_by')
    queryset = queryset.order_by('-id')

    page = paginate(queryset, None, 14, 4)

    data = pagination_dict(page)
    data.update({
        'results': UsernameChangeSerializer(page.object_list, many=True).data
    })

    request.frontend_context['PROFILE_NAME_HISTORY'] = data

    return render(request, 'misago/profile/username_history.html', {
        'profile': profile,
        'history': page.object_list,
        'count': data['count'],
    })


@profile_view_restricted_visibility
def user_ban(request, profile):
    ban = get_user_ban(profile)

    request.frontend_context['PROFILE_BAN'] = BanDetailsSerializer(ban).data

    return render(request, 'misago/profile/ban_details.html', {
        'profile': profile,
        'ban': ban,
    })


UserProfileSerializer = UserSerializer.subset_fields(
    'id', 'username', 'slug', 'email', 'joined_on', 'rank', 'title', 'avatars',
    'is_avatar_locked', 'signature', 'is_signature_locked', 'followers', 'following',
    'threads', 'posts', 'acl', 'is_followed', 'is_blocked', 'status', 'absolute_url',
    'api_url')
