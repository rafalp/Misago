from django.http import Http404

from misago.conf import settings
from misago.core.shortcuts import paginate, pagination_dict
from misago.users.online.utils import make_users_status_aware
from misago.users.serializers import UserCardSerializer


class Followers(object):
    def __init__(self, request, profile, page=0, search=None):
        queryset = self.get_queryset(profile).select_related('rank').order_by('slug')

        if not request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        if search:
            name_starts_with = search.strip().lower()
            if name_starts_with:
                queryset = queryset.filter(slug__startswith=name_starts_with)
            else:
                raise Http404()

        list_page = paginate(queryset, page, settings.MISAGO_USERS_PER_PAGE, 4)
        make_users_status_aware(request.user, list_page.object_list)

        self.users = list_page.object_list
        self.paginator = pagination_dict(list_page)

    def get_queryset(self, profile):
        return profile.followed_by

    def get_frontend_context(self):
        context = {'results': UserCardSerializer(self.users, many=True).data}
        context.update(self.paginator)
        return context

    def get_template_context(self):
        return {
            'followers': self.users,
            'count': self.paginator['count'],
        }
