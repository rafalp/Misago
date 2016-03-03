from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils.translation import ugettext as _

from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from misago.core.apipaginator import ApiPaginator
from misago.core.shortcuts import get_int_or_404, get_object_or_404

from misago.users.models import UsernameChange
from misago.users.rest_permissions import BasePermission
from misago.users.serializers.usernamechange import UsernameChangeSerializer


class UsernameChangesViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            user_id = int(request.GET.get('user'))
        except (ValueError, TypeError):
            user_id = -1

        if user_id == request.user.pk:
            return True
        elif not request.user.acl.get('can_see_users_name_history'):
            raise PermissionDenied(_("You don't have permission to "
                                     "see other users name history."))
        return True


class UsernameChangesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (UsernameChangesViewSetPermission,)
    serializer_class = UsernameChangeSerializer
    pagination_class = ApiPaginator(12, 4)

    def get_queryset(self):
        queryset = UsernameChange.objects

        if self.request.query_params.get('user'):
            user_pk = get_int_or_404(self.request.query_params.get('user'))
            queryset = get_object_or_404(
                get_user_model().objects, pk=user_pk).namechanges

        if self.request.query_params.get('search'):
            search_phrase = self.request.query_params.get('search').strip()
            if search_phrase:
                queryset = queryset.filter(
                    Q(changed_by_username__istartswith=search_phrase) |
                    Q(new_username__istartswith=search_phrase) |
                    Q(old_username__istartswith=search_phrase))

        return queryset.select_related('user', 'changed_by').order_by('-id')
