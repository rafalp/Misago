from typing import Any, List, Sequence


def remove_none_items(items_list: Sequence[Any]) -> List[Any]:
    return [i for i in items_list if i is not None]
