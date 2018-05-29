from datetime import timedelta

from django.dispatch import Signal, receiver
from django.contrib.auth import get_user_model
from django.utils import timezone

from django.db.models import Q
from misago.core.utils import ANONYMOUS_IP
from misago.conf import settings


UserModel = get_user_model()

anonymize_old_ips = Signal()
anonymize_user_content = Signal()
delete_user_content = Signal()
username_changed = Signal()


@receiver(username_changed)
def handle_name_change(sender, **kwargs):
    sender.user_renames.update(changed_by_username=sender.username)


@receiver(anonymize_old_ips)
def anonymize_old_registrations_ips(sender, **kwargs):
    anonymization_cutoff = timezone.now() - timedelta(days=settings.MISAGO_IP_STORE_TIME)
    ip_is_too_new = Q(joined_on__lt=anonymization_cutoff)
    ip_is_already_anonymized = Q(joined_from_ip=ANONYMOUS_IP)
    queryset = UserModel.objects.exclude(ip_is_too_new | ip_is_already_anonymized)

    queryset.update(joined_from_ip=ANONYMOUS_IP)

