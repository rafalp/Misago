from rest_framework import mixins, viewsets

from ..models import Rank
from ..serializers import RankSerializer


class RanksViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RankSerializer
    queryset = Rank.objects.filter(is_tab=True).order_by("order")
