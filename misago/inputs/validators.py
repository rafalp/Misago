import ipaddress
import re
from typing import Any, AnyStr, Callable, Optional, Pattern, Sequence, Union
from urllib.parse import urlsplit, urlunsplit

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


class URLValidator(RegexValidator):
    UL = "\u00a1-\uffff"  # unicode letters range (must not be a raw string)

    # IP patterns
    IPV4_RE = (
        r"(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}"
    )
    IPV6_RE = r"\[[0-9a-f:\.]+\]"  # (simple regex, validated later)

    # Host patterns
    HOSTNAME_RE = (
        r"[a-z" + UL + r"0-9](?:[a-z" + UL + r"0-9-]{0,61}[a-z" + UL + r"0-9])?"
    )
    # Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
    DOMAIN_RE = r"(?:\.(?!-)[a-z" + UL + r"0-9-]{1,63}(?<!-))*"
    TLD_RE = (
        r"\."  # dot
        r"(?!-)"  # can't start with a dash
        r"(?:[a-z" + UL + "-]{2,63}"  # domain label
        r"|xn--[a-z0-9]{1,59})"  # or punycode label
        r"(?<!-)"  # can't end with a dash
        r"\.?"  # may have a trailing dot
    )
    HOST_RE = "(" + HOSTNAME_RE + DOMAIN_RE + TLD_RE + "|localhost)"

    DEFAULT_RE = re.compile(
        r"^(?:[a-z0-9\.\-\+]*)://"  # scheme is validated separately
        r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"  # user:pass authentication
        r"(?:" + IPV4_RE + "|" + IPV6_RE + "|" + HOST_RE + ")"
        r"(?::\d{2,5})?"  # port
        r"(?:[/?#][^\s]*)?"  # resource path
        r"\Z",
        re.IGNORECASE,
    )

    _schemes: Sequence[str]
    _code: str

    def __init__(
        self, *, schemes: Optional[Sequence[str]] = None, code: str = "INVALID"
    ):
        super().__init__(self.DEFAULT_RE, code=code)

        self._schemes = schemes or ["http", "https", "ftp", "ftps"]

    def __call__(self, value: str):
        scheme = value.split("://")[0].lower()
        if scheme not in self._schemes:
            raise InputError(self._code)
            # Then check full URL
        try:
            super().__call__(value)
        except InputError as e:
            # Trivial case failed. Try for possible IDN domain
            if value:
                try:
                    scheme, netloc, path, query, fragment = urlsplit(value)
                except ValueError:  # for example, "Invalid IPv6 URL"
                    raise InputError(self._code)
                try:
                    netloc = netloc.encode("idna").decode("ascii")  # IDN -> ACE
                except UnicodeError:  # invalid domain part
                    raise e
                url = urlunsplit((scheme, netloc, path, query, fragment))
                super().__call__(url)
            else:
                raise
        else:
            # Now verify IPv6 in the netloc part
            host_match = re.search(r"^\[(.+)\](?::\d{2,5})?$", urlsplit(value).netloc)
            if host_match:
                potential_ip = host_match.groups()[0]
                try:
                    validate_ipv6_address(potential_ip)
                except InputError:
                    raise InputError(self._code)

        # The maximum length of a full host name is 253 characters per RFC 1034
        # section 3.1. It's defined to be 255 bytes or less, but this includes
        # one byte for the length of the name and one byte for the trailing dot
        # that's used to indicate absolute names in DNS.
        if len(urlsplit(value).netloc) > 253:
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
