from rest_framework import viewsets, mixins

from misago.users.models import Rank
from misago.users.serializers import RankSerializer


class RanksViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RankSerializer
    queryset = Rank.objects.filter(is_tab=True).order_by('order')
