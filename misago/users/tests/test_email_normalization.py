from ..email import normalize_email


def test_email_domain_is_normalized():
    assert normalize_email("test@eXamplE.com") == "test@example.com"


def test_email_identifier_is_not_normalized():
    assert normalize_email("tEst@example.com") == "tEst@example.com"
