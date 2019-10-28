import re
import secrets

from unidecode import unidecode


RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def get_random_string(
    length: int = 12, allowed_chars: str = RANDOM_STRING_CHARS
) -> str:
    """
    Return a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    return "".join(secrets.choice(allowed_chars) for i in range(length))


def slugify(value: str) -> str:
    value = str(value)
    value = unidecode(value)
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)
