from ...users import tokens


def test_token_can_be_created_for_user(user):
    assert tokens.make(user, "test")


def test_token_can_be_validated(user):
    token = tokens.make(user, "test")
    assert tokens.is_valid(user, "test", token)


def test_token_fails_validation_for_different_type(user):
    token = tokens.make(user, "activation")
    assert not tokens.is_valid(user, "new_password", token)


def test_token_fails_validation_for_different_user(user, other_user):
    token = tokens.make(user, "test")
    assert not tokens.is_valid(other_user, "test", token)
