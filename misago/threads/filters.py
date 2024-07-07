from dataclasses import dataclass

from django.http import HttpRequest
from django.db.models import QuerySet
from django.utils.translation import pgettext_lazy


class ThreadsFilter:
    slug: str
    name: str

    request: HttpRequest

    def __init__(self, request: HttpRequest):
        self.request = request

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
    slug: str = "my"
    name: str = pgettext_lazy("threads filter", "My threads")

    def __call__(self, queryset: QuerySet) -> QuerySet:
        if self.request.user.is_authenticated:
            return queryset.filter(starter=self.request.user)

        return queryset.empty()


@dataclass(frozen=True)
class ThreadsFilterChoice:
    name: str
    url: str
    active: bool
    filter: MyThreadsFilter
