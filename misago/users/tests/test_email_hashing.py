from ..email import get_email_hash


def test_email_hash_is_created():
    assert get_email_hash("test@example.com")


def test_email_hash_is_case_insensitive():
    assert get_email_hash("test@example.com") == get_email_hash("test@eXamplE.com")


def test_email_hash_differs_for_different_emails():
    assert get_email_hash("test@example.com") != get_email_hash("other@example.com")
