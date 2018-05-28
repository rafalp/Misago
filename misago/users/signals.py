from django.dispatch import Signal, receiver
from django.contrib.auth import get_user_model
from misago.core.utils import ANONYMOUS_IP

anonymize_user_content = Signal()
delete_user_content = Signal()
username_changed = Signal()
anonymize_old_ips = Signal()

@receiver(username_changed)
def handle_name_change(sender, **kwargs):
    sender.user_renames.update(changed_by_username=sender.username)


UserModel = get_user_model()
MISAGO_IP_STORE_TIME = 33300

@receiver(anonymize_old_ips)
def handle_old_ips(sender, **kwargs):
    for user in UserModel.objects.all():
        user.joined_from_ip = ANONYMOUS_IP
        user.save()