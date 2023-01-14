from ..validation import filter_name


def test_filter_replaces_spaces_with_underscores(db):
    assert filter_name(None, "John Doe") == "John_Doe"


def test_filter_strips_special_characters(db):
    assert filter_name(None, "John Doe!") == "John_Doe"


def test_filter_strips_unicode_strings(db):
    assert filter_name(None, "Łóżąć Bęś") == "Lozac_Bes"


def test_filter_generates_random_name_to_avoid_empty_result(db):
    user_name = filter_name(None, "__!!!")
    assert user_name
    assert len(user_name) > 5
    assert user_name.startswith("User_")


def test_filter_generates_unique_name_to_avoid_same_names(user):
    user_name = filter_name(None, user.username)

    assert user_name
    assert user_name != user.username
    assert user_name.startswith(user.username)


def test_filter_keeps_user_name_if_its_same_as_current_one(user):
    user_name = filter_name(user, user.username)
    assert user_name == user.username


def test_filter_keeps_cleaned_user_name_if_its_same_as_current_one(user):
    user.set_username("Lozac_Bes")
    user.save()

    user_name = filter_name(user, "Łóżąć Bęś")
    assert user_name == user.username
