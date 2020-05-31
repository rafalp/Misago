from typing import Any, List, Protocol, Sequence


def remove_none_items(items_list: Sequence[Any]) -> List[Any]:
    return [i for i in items_list if i is not None]


class ItemWithID(Protocol):
    id: Any


def update_list_items(
    src_list: Sequence[ItemWithID], updated_items: Sequence[ItemWithID]
) -> List[ItemWithID]:
    updated_map = {i.id: i for i in updated_items}
    return [updated_map.get(i.id, i) for i in src_list]
