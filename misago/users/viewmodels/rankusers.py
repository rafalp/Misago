from ...core.shortcuts import paginate, pagination_dict
from ..online.utils import make_users_status_aware
from ..serializers import UserCardSerializer


class RankUsers:
    def __init__(self, request, rank, page=0):
        queryset = rank.user_set.select_related(
            "rank", "ban_cache", "online_tracker"
        ).order_by("slug")

        if not request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        list_page = paginate(
            queryset,
            page,
            request.settings.users_per_page,
            request.settings.users_per_page_orphans,
        )
        make_users_status_aware(request, list_page.object_list)

        self.users = list_page.object_list
        self.paginator = pagination_dict(list_page)

    def get_frontend_context(self):
        context = {"results": UserCardSerializer(self.users, many=True).data}
        context.update(self.paginator)
        return context

    def get_template_context(self):
        return {"users": self.users, "paginator": self.paginator}
