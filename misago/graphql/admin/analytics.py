from datetime import timedelta

from ariadne import QueryType
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone

from ...threads.models import Attachment, Post, Thread
from ...users.models import DataDownload

CACHE_KEY = "misago_admin_analytics"
CACHE_LENGTH = 3600 * 4  # 4 hours

User = get_user_model()

analytics = QueryType()


@analytics.field("analytics")
def resolve_analytics(_, info, *, span):
    span = clean_span(span)
    cache_key = "%s_%s" % (CACHE_KEY, span)
    data = cache.get(cache_key)
    if not data:
        data = get_data_from_db(span)
        cache.set(cache_key, data, CACHE_LENGTH)
    return data


def clean_span(span):
    if span > 360:
        return 360
    if span < 30:
        return 30
    return span


def get_data_from_db(span):
    analytics = Analytics(span)

    return {
        "users": analytics.get_data_for_model(User, "joined_on"),
        "threads": analytics.get_data_for_model(Thread, "started_on"),
        "posts": analytics.get_data_for_model(Post, "posted_on"),
        "attachments": analytics.get_data_for_model(Attachment, "uploaded_on"),
        "dataDownloads": analytics.get_data_for_model(DataDownload, "requested_on"),
    }


class Analytics:
    def __init__(self, span):
        self.today = timezone.now()
        self.span = span

        self.cutoff = self.today - timedelta(days=span * 2)
        self.legend = self.get_legend()

    def get_legend(self):
        legend = []
        for day in range(self.span * 2):
            date = self.today - timedelta(days=day)
            legend.append(date.strftime("%x"))
        return legend

    def get_empty_data(self):
        return {k: 0 for k in self.legend}

    def get_data_for_model(self, model, date_attr):
        filter_kwarg = {"%s__gte" % date_attr: self.cutoff}
        queryset = model.objects.filter(**filter_kwarg).order_by("-pk")

        data = self.get_empty_data()
        for item in queryset.values(date_attr).iterator():
            date = item[date_attr].strftime("%x")
            if date in data:
                data[date] += 1

        values = list(data.values())
        return {
            "current": list(reversed(values[: self.span])),
            "previous": list(reversed(values[self.span :])),
        }
