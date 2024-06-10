import hmac
import hashlib
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from django.conf import settings
from django.utils import timezone

if TYPE_CHECKING:
    from ..users.models import User

TIMESTAMP_FORMAT = "%Y%m%d%H%S"


class EmailChangeTokenError(ValueError):
    pass


def create_email_change_token(user: "User", new_email: str) -> str:
    timestamp = timezone.now().strftime(TIMESTAMP_FORMAT)
    message = urlsafe_b64encode(f"{timestamp}:{new_email}".encode("utf-8"))
    signature = get_email_change_signature(user, message)

    return f"{signature}-{message.decode('utf-8')}"


def read_email_change_token(user: "User", token: str) -> str:
    if "-" not in token:
        raise EmailChangeTokenError("missing signature or message")

    signature, message = token.split("-", 1)
    if not signature or not message:
        raise EmailChangeTokenError("missing signature or message")

    if signature != get_email_change_signature(user, message.encode("utf-8")):
        raise EmailChangeTokenError("invalid signature for message")

    timestamp, email = urlsafe_b64decode(message).decode("utf-8").split(":", 1)

    created = datetime.strptime(timestamp, TIMESTAMP_FORMAT).replace(
        tzinfo=timezone.utc
    )
    expires = created + timedelta(hours=settings.MISAGO_EMAIL_CHANGE_TOKEN_EXPIRES)

    if timezone.now() > expires:
        raise EmailChangeTokenError("token expired")

    return email


def get_email_change_secret(user: "User") -> bytes:
    return (
        f"{user.pk}:{user.email_hash}:{user.password}:{settings.SECRET_KEY}"
    ).encode("utf-8")


def get_email_change_signature(user: "User", message: bytes) -> str:
    return hmac.new(get_email_change_secret(user), message, hashlib.sha256).hexdigest()
