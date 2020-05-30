import pytest

from ...errors import ListRepeatedItemsError
from ..types import bulkactionidslist


settings = {"bulk_action_limit": 5}


def test_bulkactionidslist_constraint_returns_list_type():
    type_ = bulkactionidslist(int, settings)
    assert issubclass(type_, list)


def test_bulkactionidslist_allows_list_without_repeated_items():
    type_ = bulkactionidslist(int, settings)
    assert type_.list_items_are_unique_validator([1, 2, 3]) == [1, 2, 3]


def test_bulkactionidslist_raises_value_error_if_there_are_repeated_items_in_list():
    type_ = bulkactionidslist(int, settings)
    with pytest.raises(ListRepeatedItemsError):
        type_.list_items_are_unique_validator([1, 2, 3, 3])
