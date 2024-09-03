from dataclasses import dataclass

from django.http import HttpRequest
from django.db.models import F, Q, QuerySet
from django.utils.translation import pgettext_lazy

from ..readtracker.models import ReadCategory, ReadThread
from ..readtracker.readtime import get_default_read_time


class ThreadsFilter:
    name: str
    url: str

    def __call__(self, queryset: QuerySet) -> QuerySet:
        return queryset

    def as_choice(self, base_url: str, active: bool) -> "ThreadsFilterChoice":
        return ThreadsFilterChoice(
            name=self.name,
            url=self.url,
            absolute_url=f"{base_url}{self.url}/",
            active=active,
            filter=self,
        )


class UnreadThreadsFilter(ThreadsFilter):
    name: str = pgettext_lazy("threads filter", "Unread threads")
    url: str = "unread"

    request: HttpRequest

    def __init__(self, request: HttpRequest):
        self.request = request

    def __call__(self, queryset: QuerySet) -> QuerySet:
        if self.request.user.is_anonymous:
            return queryset.none()

        read_time = get_default_read_time(self.request.settings, self.request.user)

        queryset = queryset.filter(
            last_post_on__gt=read_time,
        )

        categories_read_times = ReadCategory.objects.filter(
            user=self.request.user
        ).values_list("category_id", "read_time")

        for category_id, read_time in categories_read_times:
            queryset = queryset.exclude(
                category_id=category_id, last_post_on__lte=read_time
            )

        queryset = queryset.exclude(
            id__in=ReadThread.objects.filter(
                user=self.request.user,
                read_time__gte=F("thread__last_post_on"),
            ).values("thread_id")
        )

        return queryset


class MyThreadsFilter(ThreadsFilter):
    name: str = pgettext_lazy("threads filter", "My threads")
    url: str = "my"

    request: HttpRequest

    def __init__(self, request: HttpRequest):
        self.request = request

    def __call__(self, queryset: QuerySet) -> QuerySet:
        if self.request.user.is_authenticated:
            return queryset.filter(starter=self.request.user)

        return queryset.none()


class UnapprovedThreadsFilter(ThreadsFilter):
    name: str = pgettext_lazy("threads filter", "Unapproved threads")
    url: str = "unapproved"

    request: HttpRequest

    def __init__(self, request: HttpRequest):
        self.request = request

    def __call__(self, queryset: QuerySet) -> QuerySet:
        return queryset.filter(Q(is_unapproved=True) | Q(has_unapproved_posts=True))


@dataclass(frozen=True)
class ThreadsFilterChoice:
    name: str
    url: str
    absolute_url: str
    active: bool
    filter: MyThreadsFilter
