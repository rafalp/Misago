import ipaddress
import re
from typing import Any, AnyStr, Callable, Optional, Pattern, Sequence, Union

from .errors import Errors, InputError


Validator = Callable[[Any, Optional[Errors], Optional[Any]], None]


class MinLengthValidator:
    _min_length: int
    _code: str

    def __init__(self, min_length: int, *, code: str = "TOO_SHORT"):
        self._min_length = min_length
        self._code = code

    def __call__(self, value: Sequence[Any]):
        value_len = len(value)
        if value_len < self._min_length:
            raise InputError(self._code, f"{value_len} < {self._min_length}")


class MaxLengthValidator:
    _max_length: int
    _code: str

    def __init__(self, max_length: int, *, code: str = "TOO_LONG"):
        self._max_length = max_length
        self._code = code

    def __call__(self, value: Sequence[Any]):
        value_len = len(value)
        if value_len > self._max_length:
            raise InputError(self._code, f"{value_len} > {self._max_length}")


class MinValueValidator:
    _min_value: int
    _code: str

    def __init__(self, min_value: int, *, code: str = "TOO_SMALL"):
        self._min_value = min_value
        self._code = code

    def __call__(self, value: Union[float, int]):
        if value < self._min_value:
            raise InputError(self._code, f"{value} < {self._min_value}")


class MaxValueValidator:
    _max_value: int
    _code: str

    def __init__(self, max_value: int, *, code: str = "TOO_LARGE"):
        self._max_value = max_value
        self._code = code

    def __call__(self, value: Union[float, int]):
        if value > self._max_value:
            raise InputError(self._code, f"{value} > {self._max_value}")


class RegexValidator:
    _regex: Pattern[AnyStr]
    _code: str
    _flags: int
    _inverse_match: bool

    def __init__(
        self,
        regex: Union[str, Pattern[AnyStr]],
        *,
        code: str = "INVALID",
        flags: int = 0,
        inverse_match: bool = False,
    ):
        if flags and not isinstance(regex, str):
            raise TypeError(
                "'regex' argument must be string when 'flags' option is set"
            )

        self._regex = re.compile(regex, flags)
        self._code = code
        self._inverse_match = inverse_match

    def __call__(self, value: str):
        regex_matches = self._regex.search(value)
        invalid_input = regex_matches if self._inverse_match else not regex_matches
        if invalid_input:
            raise InputError(self._code)


class EmailValidator:
    USER_REGEX = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE,
    )
    DOMAIN_REGEX = re.compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r"((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z",
        re.IGNORECASE,
    )
    LITERAL_REGEX = re.compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r"\[([A-f0-9:\.]+)\]\Z",
        re.IGNORECASE,
    )

    _code: str
    _domain_whitelist: Optional[Sequence[str]]

    def __init__(
        self, *, code: str = "INVALID", domain_whitelist: Optional[Sequence[str]] = None
    ):
        self._code = code
        self._domain_whitelist = domain_whitelist

    def __call__(self, value: str):
        if not value or "@" not in value:
            raise InputError(self._code)

        user_part, domain_part = value.rsplit("@", 1)

        if not self.USER_REGEX.match(user_part):
            raise InputError(self._code)

        if (
            not self._domain_whitelist or domain_part not in self._domain_whitelist
        ) and not self.validate_domain_part(domain_part):
            # Try for possible IDN domain-part
            try:
                domain_part = domain_part.encode("idna").decode("ascii")
            except UnicodeError:
                pass
            else:
                if self.validate_domain_part(domain_part):
                    return
            raise InputError(self._code)

    def validate_domain_part(self, domain_part: str) -> bool:
        if self.DOMAIN_REGEX.match(domain_part):
            return True

        literal_match = self.LITERAL_REGEX.match(domain_part)
        if literal_match:
            ip_address = literal_match.group(1)
            try:
                validate_ipv46_address(ip_address)
                return True
            except InputError:
                pass
        return False


class BelongsToValidator:
    _sequence: Sequence[Any]
    _code: str
    _inverse_match: bool

    def __init__(
        self,
        sequence: Sequence[Any],
        *,
        code: str = "INVALID",
        inverse_match: bool = False,
    ):
        self._sequence = sequence
        self._code = code
        self._inverse_match = inverse_match

    def __call__(self, value: Any):
        belongs_to = value in self._sequence
        invalid_input = belongs_to if self._inverse_match else not belongs_to
        if invalid_input:
            raise InputError(self._code)


def validate_ipv4_address(value: str, *, code: str = "INVALID"):
    try:
        ipaddress.IPv4Address(value)
    except ValueError:
        raise InputError(code)


def validate_ipv6_address(value: str, *, code: str = "INVALID"):
    try:
        ipaddress.IPv6Address(value)
    except ValueError:
        raise InputError(code)


def validate_ipv46_address(value: str, *, code: str = "INVALID"):
    try:
        validate_ipv4_address(value, code=code)
    except InputError:
        validate_ipv6_address(value, code=code)
