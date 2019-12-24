from typing import Any, List, Sequence


def clear_list(items_list: Sequence[Any]) -> List[Any]:
    return [i for i in items_list if i is not None]
