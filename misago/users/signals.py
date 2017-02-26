from django.dispatch import Signal, receiver


delete_user_content = Signal()
username_changed = Signal()


@receiver(username_changed)
def handle_name_change(sender, **kwargs):
    sender.user_renames.update(changed_by_username=sender.username)
