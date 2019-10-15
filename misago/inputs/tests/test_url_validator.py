import pytest

from ..errors import InputError
from ..validators import URLValidator


def test_url_validator_raises_invalid_error_for_invalid_value():
    validator = URLValidator()
    with pytest.raises(InputError) as excinfo:
        validator("invalid")

    assert excinfo.value.code == "INVALID"


def test_url_validator_raises_custom_code_for_invalid_value():
    validator = URLValidator(code="CUSTOM")
    with pytest.raises(InputError) as excinfo:
        validator("invalid")

    assert excinfo.value.code == "CUSTOM"


def test_url_validator_raises_invalid_error_for_disallowed_scheme():
    validator = URLValidator(schemes=["ftp"])
    with pytest.raises(InputError) as excinfo:
        validator("http://example.com")

    assert excinfo.value.code == "INVALID"


def test_url_validator_allows_url_with_specified_scheme():
    validator = URLValidator(schemes=["ftp"])
    validator("ftp://example.com")


def test_url_validator_allows_url():
    validator = URLValidator()
    validator("http://example.com")


def test_url_validator_allows_url_with_querystring():
    validator = URLValidator()
    validator("http://example.com/?query=string")


def test_url_validator_allows_url_with_path():
    validator = URLValidator()
    validator("http://example.com/path/index.html")


def test_url_validator_allows_url_with_ip_address():
    validator = URLValidator()
    validator("http://127.0.0.1")


def test_url_validator_allows_url_with_ip_address_and_port():
    validator = URLValidator()
    validator("http://127.0.0.1:8000")


def test_url_validator_allows_url_with_querystring():
    validator = URLValidator()
    validator("http://example.com/?query=string")


def test_url_validator_allows_url_with_non_standard_scheme():
    validator = URLValidator(schemes=["git+ssh"])
    validator("git+ssh://git@github.com/example/hg-git.git")
