from misago.conf import settings
from misago.users.activepostersranking import get_active_posters_ranking
from misago.users.online.utils import make_users_status_aware
from misago.users.serializers import UserCardSerializer


class ActivePosters(object):
    def __init__(self, request):
        ranking = get_active_posters_ranking()
        make_users_status_aware(request.user, ranking['users'], fetch_state=True)

        self.count = ranking['users_count']
        self.tracked_period = settings.MISAGO_RANKING_LENGTH
        self.users = ranking['users']

    def get_frontend_context(self):
        return {
            'tracked_period': self.tracked_period,
            'results': ScoredUserSerializer(self.users, many=True).data,
            'count': self.count,
        }

    def get_template_context(self):
        return {
            'tracked_period': self.tracked_period,
            'users': self.users,
            'users_count': self.count,
        }


ScoredUserSerializer = UserCardSerializer.extend_fields('meta')
