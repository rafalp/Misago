import pytest

from ..errors import InputError
from ..validators import EmailValidator


def test_email_validator_raises_invalid_error_for_invalid_value():
    validator = EmailValidator()
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.code == "INVALID"


def test_email_validator_raises_invalid_error_for_invalid_user_part():
    validator = EmailValidator()
    with pytest.raises(InputError) as excinfo:
        validator("test @domain.com")

    assert excinfo.value.code == "INVALID"


def test_email_validator_raises_invalid_error_for_invalid_domain_part():
    validator = EmailValidator()
    with pytest.raises(InputError) as excinfo:
        validator("user@domain")

    assert excinfo.value.code == "INVALID"


def test_email_validator_raises_custom_code_for_invalid_value():
    validator = EmailValidator(code="CUSTOM")
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.code == "CUSTOM"


def test_email_validator_allows_ipv4_for_domain():
    validator = EmailValidator()
    validator("user@[127.0.0.1]")


def test_email_validator_allows_ipv6_for_domain():
    validator = EmailValidator()
    validator("user@[2001:0db8:85a3:0000:0000:8a2e:0370:7334]")


def test_email_validator_allows_whitelisted_domain():
    validator = EmailValidator(domain_whitelist=["domain"])
    validator("user@domain")


def test_email_validator_allows_valid_email():
    validator = EmailValidator()
    validator("user@example.com")


def test_bulk_test_email_validator_compliance_with_django_implementation():
    # Runs test cases from Django tests suite against email validator
    # https://github.com/django/django/blob/master/tests/validators/tests.py#L43
    validator = EmailValidator()

    passsing_cases = (
        "email@here.com",
        "weirder-email@here.and.there.com",
        "email@[127.0.0.1]",
        "email@[2001:dB8::1]",
        "email@[2001:dB8:0:0:0:0:0:1]",
        "email@[::fffF:127.0.0.1]",
        "example@valid-----hyphens.com",
        "example@valid-with-hyphens.com",
        "test@domain.with.idn.tld.उदाहरण.परीक्षा",
        '"test@test"@example.com',
        "example@atm.%s" % ("a" * 63),
        "example@%s.atm" % ("a" * 63),
        "example@%s.%s.atm" % ("a" * 63, "b" * 10),
        '"\\\011"@here.com',
        "a@%s.us" % ("a" * 63),
    )

    for case in passsing_cases:
        validator(case)

    failing_cases = (
        "example@atm.%s" % ("a" * 64),
        "example@%s.atm.%s" % ("b" * 64, "a" * 63),
        None,
        "",
        "abc",
        "abc@",
        "abc@bar",
        "a @x.cz",
        "abc@.com",
        "something@@somewhere.com",
        "email@127.0.0.1",
        "email@[127.0.0.256]",
        "email@[2001:db8::12345]",
        "email@[2001:db8:0:0:0:0:1]",
        "email@[::ffff:127.0.0.256]",
        "example@invalid-.com",
        "example@-invalid.com",
        "example@invalid.com-",
        "example@inv-.alid-.com",
        "example@inv-.-alid.com",
        'test@example.com\n\n<script src="x.js">',
        # Quoted-string format (CR not allowed)
        '"\\\012"@here.com',
        "trailingdot@shouldfail.com.",
        # Max length of domain name labels is 63 characters per RFC 1034.
        "a@%s.us" % ("a" * 64),
        # Trailing newlines in username or domain not allowed
        "a@b.com\n",
        "a\n@b.com",
        '"test@test"\n@example.com',
        "a@[127.0.0.1]\n",
    )

    for case in failing_cases:
        with pytest.raises(InputError) as excinfo:
            print(case)
            validator(case)

        assert excinfo.value.code == "INVALID"
