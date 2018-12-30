from ..utils import HASH_LENGTH, get_file_hash


def test_empty_file_hash_is_zeroes(mocker):
    empty_file = mocker.Mock(size=0)
    assert get_file_hash(empty_file) == "0" * HASH_LENGTH
