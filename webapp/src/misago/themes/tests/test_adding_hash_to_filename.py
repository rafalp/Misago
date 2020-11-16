from ..uploadto import add_hash_to_filename


def test_hash_is_added_before_file_extension():
    filename = add_hash_to_filename("hash", "test.jpg")
    assert filename == "test.hash.jpg"


def test_hash_is_added_before_file_extension_in_filename_with_multiple_dots():
    filename = add_hash_to_filename("hash", "test.image.jpg")
    assert filename == "test.image.hash.jpg"


def test_hash_is_not_added_to_filename_if_it_already_contains_it():
    filename = add_hash_to_filename("hash", "test.hash.jpg")
    assert filename == "test.hash.jpg"
