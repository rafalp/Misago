from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

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
    queryset = UsernameChange.objects
    paginate_by = 20

    def get_queryset(self):
        queryset = UsernameChange.objects.select_related('user', 'changed_by')
        user = self.request.query_params.get('user', None)
        if user is not None:
            try:
                queryset = queryset.filter(user_id=int(user))
            except (ValueError, TypeError):
                queryset = queryset.none()
        return queryset.order_by('-id')
