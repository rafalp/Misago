from enum import StrEnum

from django.db.models import IntegerChoices
from django.utils.translation import pgettext_lazy


class NotificationVerb(StrEnum):
    REPLIED = "REPLIED"
    INVITED = "INVITED"


class ThreadNotifications(IntegerChoices):
    NONE = 0, pgettext_lazy("notification type", "Don't notify")
    DONT_EMAIL = 1, pgettext_lazy(
        "notification type", "Notify without sending an e-mail"
    )
    SEND_EMAIL = 2, pgettext_lazy("notification type", "Notify with an e-mail")
