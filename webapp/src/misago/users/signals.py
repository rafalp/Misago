from collections import OrderedDict
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.dispatch import Signal, receiver
from django.utils import timezone
from django.utils.translation import gettext as _

from ..core.pgutils import chunk_queryset
from .models import AuditTrail, DataDownload
from .profilefields import profilefields

User = get_user_model()

anonymize_user_data = Signal()
archive_user_data = Signal()
delete_user_content = Signal()
remove_old_ips = Signal()
username_changed = Signal()


@receiver(archive_user_data)
def archive_user_details(sender, archive=None, **kwargs):
    archive.add_dict(
        "details",
        OrderedDict(
            [
                (_("Username"), sender.username),
                (_("E-mail"), sender.email),
                (_("Joined on"), sender.joined_on),
                (_("Joined from ip"), sender.joined_from_ip or "unavailable"),
            ]
        ),
    )


@receiver(archive_user_data)
def archive_user_profile_fields(sender, archive=None, **kwargs):
    clean_profile_fields = OrderedDict()
    for profile_fields_group in profilefields.get_fields_groups():
        for profile_field in profile_fields_group["fields"]:
            if sender.profile_fields.get(profile_field.fieldname):
                field_value = sender.profile_fields[profile_field.fieldname]
                clean_profile_fields[str(profile_field.label)] = field_value

    if clean_profile_fields:
        archive.add_dict("profile_fields", clean_profile_fields)


@receiver(archive_user_data)
def archive_user_avatar(sender, archive=None, **kwargs):
    archive.add_model_file(sender.avatar_tmp, directory="avatar", prefix="tmp")
    archive.add_model_file(sender.avatar_src, directory="avatar", prefix="src")
    for avatar in sender.avatar_set.iterator():
        archive.add_model_file(avatar.image, directory="avatar", prefix=avatar.size)


@receiver(archive_user_data)
def archive_user_audit_trail(sender, archive=None, **kwargs):
    for audit_trail in chunk_queryset(sender.audittrail_set):
        item_name = audit_trail.created_on.strftime("%H%M%S-audit-trail")
        archive.add_text(item_name, audit_trail.ip_address, date=audit_trail.created_on)


@receiver(archive_user_data)
def archive_user_name_history(sender, archive=None, **kwargs):
    for name_change in sender.namechanges.order_by("id").iterator():
        item_name = name_change.changed_on.strftime("%H%M%S-name-change")
        archive.add_dict(
            item_name,
            OrderedDict(
                [
                    (_("New username"), name_change.new_username),
                    (_("Old username"), name_change.old_username),
                ]
            ),
            date=name_change.changed_on,
        )


@receiver(username_changed)
def handle_name_change(sender, **kwargs):
    sender.user_renames.update(changed_by_username=sender.username)


@receiver(remove_old_ips)
def remove_old_registrations_ips(sender, *, ip_storage_time, **kwargs):
    datetime_cutoff = timezone.now() - timedelta(days=ip_storage_time)
    ip_is_too_new = Q(joined_on__gt=datetime_cutoff)
    ip_is_already_removed = Q(joined_from_ip__isnull=True)

    queryset = User.objects.exclude(ip_is_too_new | ip_is_already_removed)
    queryset.update(joined_from_ip=None)


@receiver(remove_old_ips)
def remove_old_audit_trails(sender, *, ip_storage_time, **kwargs):
    removal_cutoff = timezone.now() - timedelta(days=ip_storage_time)
    AuditTrail.objects.filter(created_on__lte=removal_cutoff).delete()


@receiver(anonymize_user_data)
def delete_data_downloads(sender, **kwargs):
    for data_download in chunk_queryset(sender.datadownload_set):
        data_download.delete()
