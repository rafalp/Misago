from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import six
from django.views import View

from misago.acl import add_acl
from misago.core.shortcuts import paginate, pagination_dict, validate_slug
from misago.users.bans import get_user_ban
from misago.users.online.utils import get_user_status
from misago.users.pages import user_profile
from misago.users.serializers import BanDetailsSerializer, UsernameChangeSerializer, UserSerializer
from misago.users.viewmodels import Followers, Follows, UserPosts, UserThreads


UserModel = get_user_model()


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        profile = self.get_profile(request, kwargs.pop('pk'), kwargs.pop('slug'))

        # resolve that we can display requested section
        sections = user_profile.get_sections(request, profile)
        active_section = self.get_active_section(sections)

        if not active_section:
            raise Http404()

        profile.status = get_user_status(request.user, profile)
        context_data = self.get_context_data(request, profile)

        self.complete_frontend_context(request, profile, sections)
        self.complete_context_data(request, profile, sections, context_data)

        return render(request, self.template_name, context_data)

    def get_profile(self, request, pk, slug):
        queryset = UserModel.objects.select_related('rank', 'online_tracker', 'ban_cache')

        profile = get_object_or_404(queryset, pk=pk)

        if not profile.is_active and not request.user.is_staff:
            raise Http404()

        validate_slug(profile, slug)
        add_acl(request.user, profile)

        return profile

    def get_active_section(self, sections):
        for section in sections:
            if section['is_active']:
                return section

    def get_context_data(self, request, profile):
        return {}

    def complete_frontend_context(self, request, profile, sections):
        request.frontend_context['PROFILE_PAGES'] = []
        for section in sections:
            request.frontend_context['PROFILE_PAGES'].append({
                'name': six.text_type(section['name']),
                'icon': section['icon'],
                'meta': section.get('metadata'),
                'component': section['component'],
            })

        request.frontend_context['PROFILE'] = UserProfileSerializer(
            profile, context={'user': request.user}
        ).data

        if not profile.is_active:
            request.frontend_context['PROFILE']['is_active'] = False

    def complete_context_data(self, request, profile, sections, context):
        context['profile'] = profile

        context['sections'] = sections
        for section in sections:
            if section['is_active']:
                context['active_section'] = section
                break

        if request.user.is_authenticated:
            is_authenticated_user = profile.pk == request.user.pk
            context.update({
                'is_authenticated_user': is_authenticated_user,
                'show_email': is_authenticated_user,
            })

            if not context['show_email']:
                context['show_email'] = request.user.acl_cache['can_see_users_emails']
        else:
            context.update({
                'is_authenticated_user': False,
                'show_email': False,
            })


class LandingView(ProfileView):
    def get(self, request, *args, **kwargs):
        profile = self.get_profile(request, kwargs.pop('pk'), kwargs.pop('slug'))

        return redirect(user_profile.get_default_link(), slug=profile.slug, pk=profile.pk)


class UserPostsView(ProfileView):
    template_name = 'misago/profile/posts.html'

    def get_context_data(self, request, profile):
        feed = UserPosts(request, profile)

        request.frontend_context['POSTS'] = feed.get_frontend_context()
        return feed.get_template_context()


class UserThreadsView(ProfileView):
    template_name = 'misago/profile/threads.html'

    def get_context_data(self, request, profile):
        feed = UserThreads(request, profile)

        request.frontend_context['POSTS'] = feed.get_frontend_context()
        return feed.get_template_context()


class UserFollowersView(ProfileView):
    template_name = 'misago/profile/followers.html'

    def get_context_data(self, request, profile):
        users = Followers(request, profile)

        request.frontend_context['PROFILE_FOLLOWERS'] = users.get_frontend_context()
        return users.get_template_context()


class UserFollowsView(ProfileView):
    template_name = 'misago/profile/follows.html'

    def get_context_data(self, request, profile):
        users = Follows(request, profile)

        request.frontend_context['PROFILE_FOLLOWS'] = users.get_frontend_context()
        return users.get_template_context()


class UserUsernameHistoryView(ProfileView):
    template_name = 'misago/profile/username_history.html'

    def get_context_data(self, request, profile):
        queryset = profile.namechanges.select_related('user', 'changed_by')
        queryset = queryset.order_by('-id')

        page = paginate(queryset, None, 14, 4)

        data = pagination_dict(page)
        data.update({'results': UsernameChangeSerializer(page.object_list, many=True).data})

        request.frontend_context['PROFILE_NAME_HISTORY'] = data

        return {
            'history': page.object_list,
            'count': data['count'],
        }


class UserBanView(ProfileView):
    template_name = 'misago/profile/ban_details.html'

    def get_context_data(self, request, profile):
        ban = get_user_ban(profile)

        request.frontend_context['PROFILE_BAN'] = BanDetailsSerializer(ban).data

        return {
            'ban': ban,
        }


UserProfileSerializer = UserSerializer.subset_fields(
    'id', 'username', 'slug', 'email', 'joined_on', 'rank', 'title', 'avatars', 'is_avatar_locked',
    'signature', 'is_signature_locked', 'followers', 'following', 'threads', 'posts', 'acl',
    'is_followed', 'is_blocked', 'status', 'api', 'url'
)
