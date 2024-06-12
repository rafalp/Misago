from dataclasses import dataclass
from typing import Callable, Optional

from django.http import HttpRequest
from django.urls import reverse


class Menu:
    __slots__ = ("items",)

    def __init__(self):
        self.items: list["MenuItem"] = []

    def add_item(
        self,
        *,
        key: str,
        url_name: str,
        label: str,
        icon: str | None = None,
        after: str | None = None,
        before: str | None = None,
        visible: Callable[[HttpRequest], bool] | None = None,
    ) -> "MenuItem":
        if after and before:
            raise ValueError("'after' and 'before' can't be used together.")

        item = MenuItem(
            key=key,
            url_name=url_name,
            label=label,
            icon=icon,
            visible=visible,
        )

        if after or before:
            new_items: list["MenuItem"] = []
            for other_item in self.items:
                if other_item.key == after:
                    new_items.append(other_item)
                    new_items.append(item)
                elif other_item.key == before:
                    new_items.append(item)
                    new_items.append(other_item)
                else:
                    new_items.append(other_item)
            self.items = new_items

            if item not in self.items:
                other_key = after or before
                raise ValueError(f"Item with key '{other_key}' doesn't exist.")
        else:
            self.items.append(item)

        return item

    def bind_to_request(self, request: HttpRequest) -> "BoundMenu":
        bound_items: list["BoundMenuItem"] = []
        for item in self.items:
            if bound_item := item.bind_to_request(request):
                bound_items.append(bound_item)

        return BoundMenu(bound_items)


class BoundMenu:
    __slots__ = ("active", "items")

    active: Optional["BoundMenuItem"]
    items: list["BoundMenuItem"]

    def __init__(self, items: list["BoundMenuItem"]):
        self.active: Optional["BoundMenuItem"] = None
        self.items: list["BoundMenuItem"] = items

        for item in items:
            if item.active:
                self.active = item
                break


@dataclass(frozen=True)
class MenuItem:
    __slots__ = ("key", "url_name", "label", "icon", "visible")

    key: str
    url_name: str
    label: str
    icon: str | None
    visible: Callable[[HttpRequest], bool] | None

    def bind_to_request(self, request: HttpRequest) -> Optional["BoundMenuItem"] | None:
        if self.visible and not self.visible(request):
            return None

        reversed_url = reverse(self.url_name)

        return BoundMenuItem(
            active=request.path_info.startswith(reversed_url),
            key=self.key,
            url=reversed_url,
            label=str(self.label),
            icon=self.icon,
        )


@dataclass(frozen=True)
class BoundMenuItem:
    __slots__ = ("active", "key", "url", "label", "icon")

    active: bool
    key: str
    url: str
    label: str
    icon: str | None
