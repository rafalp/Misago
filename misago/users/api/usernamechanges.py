from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.response import Response

from ...core.shortcuts import get_int_or_404, paginate, pagination_dict
from ..models import UsernameChange
from ..serializers import UsernameChangeSerializer
from .rest_permissions import BasePermission

User = get_user_model()


class UsernameChangesViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            user_pk = int(request.query_params.get("user"))
        except (ValueError, TypeError):
            user_pk = -1

        if user_pk == request.user.pk:
            return True
        if not request.user_acl.get("can_see_users_name_history"):
            raise PermissionDenied(
                _("You don't have permission to see other users name history.")
            )
        return True


class UsernameChangesViewSet(viewsets.GenericViewSet):
    permission_classes = (UsernameChangesViewSetPermission,)
    serializer_class = UsernameChangeSerializer

    def get_queryset(self):
        queryset = UsernameChange.objects

        if self.request.query_params.get("user"):
            user_pk = get_int_or_404(self.request.query_params.get("user"))
            queryset = get_object_or_404(User.objects, pk=user_pk).namechanges

        if self.request.query_params.get("search"):
            search_phrase = self.request.query_params.get("search").strip()
            if search_phrase:
                queryset = queryset.filter(
                    Q(changed_by_username__istartswith=search_phrase)
                    | Q(new_username__istartswith=search_phrase)
                    | Q(old_username__istartswith=search_phrase)
                )

        return queryset.select_related("user", "changed_by").order_by("-id")

    def list(self, request):
        page = get_int_or_404(request.query_params.get("page", 0))
        if page == 1:
            page = 0  # api allows explicit first page

        queryset = self.get_queryset()

        list_page = paginate(queryset, page, 12, 4)

        data = pagination_dict(list_page)
        data.update(
            {"results": UsernameChangeSerializer(list_page.object_list, many=True).data}
        )

        return Response(data)
