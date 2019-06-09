from ..activepostersranking import get_active_posters_ranking
from ..online.utils import make_users_status_aware
from ..serializers import UserCardSerializer


class ActivePosters:
    def __init__(self, request):
        ranking = get_active_posters_ranking()
        make_users_status_aware(request, ranking["users"], fetch_state=True)

        self.count = ranking["users_count"]
        self.tracked_period = request.settings.top_posters_ranking_length
        self.users = ranking["users"]

    def get_frontend_context(self):
        return {
            "tracked_period": self.tracked_period,
            "results": ScoredUserSerializer(self.users, many=True).data,
            "count": self.count,
        }

    def get_template_context(self):
        return {
            "tracked_period": self.tracked_period,
            "users": self.users,
            "users_count": self.count,
        }


ScoredUserSerializer = UserCardSerializer.extend_fields("meta")
