import datetime
import hashlib
import hmac
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import timedelta
from enum import StrEnum
from typing import TYPE_CHECKING

from django.conf import settings
from django.utils import timezone
from django.utils.translation import pgettext

if TYPE_CHECKING:
    from ..users.models import User

TIMESTAMP_FORMAT = "%Y%m%d%H%S"


class EmailChangeTokenErrorCode(StrEnum):
    PAYLOAD_MISSING = "PAYLOAD-MISSING"
    SIGNATURE_INVALID = "SIGNATURE-INVALID"
    SIGNATURE_MISSING = "SIGNATURE-MISSING"
    TOKEN_EXPIRED = "TOKEN-EXPIRED"
    TOKEN_INVALID = "TOKEN-INVALID"


class EmailChangeTokenError(ValueError):
    code: EmailChangeTokenErrorCode

    def __init__(self, code: EmailChangeTokenErrorCode):
        self.code = code

    def __str__(self):
        if self.code == EmailChangeTokenErrorCode.PAYLOAD_MISSING:
            return pgettext(
                "email change token error",
                "Mail change confirmation link is missing a payload.",
            )
        if self.code == EmailChangeTokenErrorCode.TOKEN_EXPIRED:
            return pgettext(
                "email change token error",
                "Mail change confirmation link has expired.",
            )
        if self.code == EmailChangeTokenErrorCode.TOKEN_INVALID:
            return pgettext(
                "email change token error",
                "Mail change confirmation link is invalid.",
            )
        if self.code == EmailChangeTokenErrorCode.SIGNATURE_INVALID:
            return pgettext(
                "email change token error",
                "Mail change confirmation link has invalid signature.",
            )
        if self.code == EmailChangeTokenErrorCode.SIGNATURE_MISSING:
            return pgettext(
                "email change token error",
                "Mail change confirmation link is missing a signature.",
            )

        return self.code.value


def create_email_change_token(user: "User", new_email: str) -> str:
    timestamp = timezone.now().strftime(TIMESTAMP_FORMAT)
    payload = urlsafe_b64encode(f"{timestamp}:{new_email}".encode("utf-8"))
    signature = get_email_change_signature(user, payload)

    return f"{signature}-{payload.decode('utf-8')}"


def read_email_change_token(user: "User", token: str) -> str:
    if "-" not in token:
        raise EmailChangeTokenError(EmailChangeTokenErrorCode.TOKEN_INVALID)

    signature, payload = token.split("-", 1)
    if not signature:
        raise EmailChangeTokenError(EmailChangeTokenErrorCode.SIGNATURE_MISSING)
    if not payload:
        raise EmailChangeTokenError(EmailChangeTokenErrorCode.PAYLOAD_MISSING)

    if signature != get_email_change_signature(user, payload.encode("utf-8")):
        raise EmailChangeTokenError(EmailChangeTokenErrorCode.SIGNATURE_INVALID)

    timestamp, email = urlsafe_b64decode(payload).decode("utf-8").split(":", 1)

    created = datetime.datetime.strptime(timestamp, TIMESTAMP_FORMAT).replace(
        tzinfo=datetime.timezone.utc
    )
    expires = created + timedelta(hours=settings.MISAGO_EMAIL_CHANGE_TOKEN_EXPIRES)

    if timezone.now() > expires:
        raise EmailChangeTokenError(EmailChangeTokenErrorCode.TOKEN_EXPIRED)

    return email


def get_email_change_secret(user: "User") -> bytes:
    return (
        f"{user.pk}:{user.email_hash}:{user.password}:{settings.SECRET_KEY}"
    ).encode("utf-8")


def get_email_change_signature(user: "User", payload: bytes) -> str:
    return hmac.new(get_email_change_secret(user), payload, hashlib.sha256).hexdigest()
