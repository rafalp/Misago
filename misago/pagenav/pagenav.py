from dataclasses import dataclass
from typing import Callable, Optional

from django.http import HttpRequest


class PageNav:
    __slots__ = ("items",)

    def __init__(self):
        self.items: list["PageNavItem"] = []

    def add_item(
        self,
        *,
        key: str,
        url: str,
        label: str,
        icon: str | None = None,
        after: str | None = None,
        before: str | None = None,
        visible: Callable[[HttpRequest], bool] | None = None,
    ) -> "PageNavItem":
        if after and before:
            raise ValueError("'after' and 'before' can't be used together.")

        item = PageNavItem(
            key=key,
            url=url,
            label=label,
            icon=icon,
            visible=visible,
        )

        if after or before:
            new_items: list["PageNavItem"] = []
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

    def get_items(self, request: HttpRequest) -> list["BoundPageNavItem"]:
        final_items: list["BoundPageNavItem"] = []
        for item in self.items:
            if bound_item := item.bind_to_request(request):
                final_items.append(bound_item)
        return final_items


@dataclass(frozen=True)
class PageNavItem:
    __slots__ = ("key", "url", "label", "icon", "visible")

    key: str
    url: str
    label: str
    icon: str | None
    visible: Callable[[HttpRequest], bool] | None

    def bind_to_request(
        self, request: HttpRequest
    ) -> Optional["BoundPageNavItem"] | None:
        if self.visible and not self.visible(request):
            return None

        return BoundPageNavItem(
            active=request.path_info.startswith(self.url),
            key=self.key,
            url=self.url,
            label=self.label,
            icon=self.icon,
        )


@dataclass(frozen=True)
class BoundPageNavItem:
    __slots__ = ("active", "key", "url", "label", "icon")

    active: bool
    key: str
    url: str
    label: str
    icon: str | None
