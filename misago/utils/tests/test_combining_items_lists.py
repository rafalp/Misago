from ..lists import update_list_items


class User:
    id: int
    name: str

    def __init__(self, id_, name):
        self.id = id_
        self.name = name


def test_empty_src_list_is_not_combined_with_other_lists():
    src_list = []
    updated_list = [User(1, "Bob")]

    result = update_list_items(src_list, updated_list)
    assert result == []


def test_extra_updated_list_items_arent_added_to_result_list():
    src_list = [User(2, "Alice")]
    updated_list = [User(1, "Bob")]

    result = update_list_items(src_list, updated_list)
    assert result == src_list


def test_list_items_are_updated():
    src_list = [User(1, "Bob"), User(2, "Alice")]
    updated_list = [User(1, "Bobby")]

    result = update_list_items(src_list, updated_list)
    assert result == [updated_list[0], src_list[1]]
