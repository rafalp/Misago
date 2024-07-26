from dataclasses import dataclass

from django.http import HttpRequest
from django.db.models import Q, QuerySet
from django.utils.translation import pgettext_lazy


class ThreadsFilter:
    name: str
    slug: str

    def __call__(self, queryset: QuerySet) -> QuerySet:
        return queryset

    def as_choice(self, base_url: str, active: bool) -> "ThreadsFilterChoice":
        return ThreadsFilterChoice(
            name=self.name,
            url=f"{base_url}{self.slug}/",
            active=active,
            filter=self,
        )


class MyThreadsFilter(ThreadsFilter):
    name: str = pgettext_lazy("threads filter", "My threads")
    slug: str = "my"

    request: HttpRequest

    def __init__(self, request: HttpRequest):
        self.request = request

    def __call__(self, queryset: QuerySet) -> QuerySet:
        if self.request.user.is_authenticated:
            return queryset.filter(starter=self.request.user)

        return queryset.none()


class UnapprovedThreadsFilter(ThreadsFilter):
    name: str = pgettext_lazy("threads filter", "Unapproved threads")
    slug: str = "unapproved"

    request: HttpRequest

    def __init__(self, request: HttpRequest):
        self.request = request

    def __call__(self, queryset: QuerySet) -> QuerySet:
        return queryset.filter(Q(is_unapproved=True) | Q(has_unapproved_posts=True))


@dataclass(frozen=True)
class ThreadsFilterChoice:
    name: str
    url: str
    active: bool
    filter: MyThreadsFilter
