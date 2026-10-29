from collections.abc import ItemsView, Iterator, KeysView, Mapping, ValuesView
from copy import deepcopy
from dataclasses import dataclass
from functools import cached_property
from typing import Any

from django.core.cache import cache

from ..cache.enums import CacheName
from .hooks import serialize_group_plugin_data_hook
from .models import Group


@dataclass(frozen=True)
class GroupProxy:
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

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "user_title": self.user_title,
            "color": self.color,
            "icon": self.icon,
            "css_suffix": self.css_suffix,
            "is_page": self.is_page,
            "is_hidden": self.is_hidden,
            "plugin_data": self.plugin_data,
        }


class GroupsProxy(Mapping[int, GroupProxy]):
    _cache_versions: dict[str, str]

    def __init__(self, cache_versions: dict[str, str]):
        self._cache_versions = cache_versions

    @cached_property
    def _data(self) -> dict[int, GroupProxy]:
        self._ready = True

        if data := self._get_data_from_cache():
            return self._hydrate_data(data)

        else:
            data = self._get_data_from_db()
            cache.set(self._get_cache_key(), data)
            return self._hydrate_data(data)

    def _get_data_from_cache(self) -> list[dict[str, Any]]:
        return cache.get(self._get_cache_key())

    def _get_cache_key(self) -> str:
        return f"groups:{self._cache_versions[CacheName.GROUPS]}"

    def _get_data_from_db(self) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = []

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

        for result in queryset:
            result["plugin_data"] = serialize_group_plugin_data(deepcopy(result))
            data.append(result)

        return data

    def _hydrate_data(self, data: list[dict]) -> dict[int, GroupProxy]:
        return {group["id"]: GroupProxy(**group) for group in data}

    def __bool__(self) -> bool:
        return bool(self._data)

    def __contains__(self, group: Group | GroupProxy | int) -> bool:
        group_id = group if isinstance(group, int) else group.id
        return group_id in self._data

    def __getitem__(self, group_id: int) -> GroupProxy:
        return self._data[group_id]

    def __iter__(self) -> Iterator[int]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def keys(self) -> KeysView[int]:
        return self._data.keys()

    def values(self) -> ValuesView[GroupProxy]:
        return self._data.values()

    def items(self) -> ItemsView[int, GroupProxy]:
        return self._data.items()

    def get(self, group_id: int) -> GroupProxy | None:
        return self._data.get(group_id)


def serialize_group_plugin_data(result: dict[str, Any]) -> dict[str, Any]:
    return serialize_group_plugin_data_hook(_serialize_group_plugin_data_action, result)


def _serialize_group_plugin_data_action(result: dict[str, Any]) -> dict[str, Any]:
    return {}
