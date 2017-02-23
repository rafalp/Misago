from misago.conf import settings
from misago.core.shortcuts import paginate, pagination_dict
from misago.users.online.utils import make_users_status_aware
from misago.users.serializers import UserCardSerializer


class RankUsers(object):
    def __init__(self, request, rank, page=0):
        queryset = rank.user_set.select_related(
            'rank',
            'ban_cache',
            'online_tracker',
        ).order_by('slug')

        if not request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        list_page = paginate(queryset, page, settings.MISAGO_USERS_PER_PAGE, 4)
        make_users_status_aware(request.user, list_page.object_list)

        self.users = list_page.object_list
        self.paginator = pagination_dict(list_page)

    def get_frontend_context(self):
        context = {'results': UserCardSerializer(self.users, many=True).data}
        context.update(self.paginator)
        return context

    def get_template_context(self):
        return {
            'users': self.users,
            'paginator': self.paginator,
        }
