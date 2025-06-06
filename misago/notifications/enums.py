from django.db.models import IntegerChoices
from django.utils.translation import pgettext_lazy


class ThreadNotifications(IntegerChoices):
    NONE = 0, pgettext_lazy("notification type", "Don't notify")
    SITE_ONLY = 1, pgettext_lazy("notification type", "Notify on site only")
    SITE_AND_EMAIL = 2, pgettext_lazy(
        "notification type", "Notify on site and with e-mail"
    )
