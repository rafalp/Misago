from typing import TypedDict

from django.core.cache import cache

from ..cache.enums import CacheName
from .models import Group


class GroupProxy(TypedDict):
    id: int
    name: str
    slug: str
    user_title: str | None
    color: str | None
    icon: str | None
    css_suffix: str | None
    is_page: bool
    is_hidden: bool
    plugin_data: dict


class GroupsProxy:
    _cache_versions: dict[str, str]
    _ready: bool
    _data: dict[int, GroupProxy]

    def __init__(self, cache_versions: dict[str, str]):
        self._cache_versions = cache_versions
        self._ready = False

    def __getitem__(self, key) -> GroupProxy:
        if not self._ready:
            self._ready_data()

        try:
            return self._data[key]
        except KeyError as exc:
            raise KeyError(key) from exc

    def _ready_data(self):
        self._ready = True

        if data := self._get_data_from_cache():
            self._data = data

        else:
            self._data = self._get_data_from_db()
            cache.set(self._get_cache_key(), self._data)

    def _get_data_from_cache(self) -> dict[int, GroupProxy]:
        return cache.get(self._get_cache_key())

    def _get_cache_key(self) -> str:
        return f"groups:{self._cache_versions[CacheName.GROUPS]}"

    def _get_data_from_db(self) -> dict[int, GroupProxy]:
        data: dict[int, GroupProxy] = {}

        queryset = Group.objects.values(
            "id",
            "name",
            "slug",
            "user_title",
            "color",
            "icon",
            "css_suffix",
            "is_page",
            "is_hidden",
            "plugin_data",
        ).order_by("ordering")

        for group in queryset:
            data[group["id"]] = group

        return data

    def items(self) -> list[tuple[int, GroupProxy]]:
        if not self._ready:
            self._ready_data()

        return list(self._data.items())

    def list(self) -> list[GroupProxy]:
        if not self._ready:
            self._ready_data()

        return list(self._data.values())
