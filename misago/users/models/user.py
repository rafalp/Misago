from hashlib import md5
from typing import Optional, Union

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.contrib.postgres.indexes import GinIndex
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import pgettext, pgettext_lazy

from ...acl.models import Role
from ...conf import settings
from ...core.utils import slugify
from ...notifications.threads import ThreadNotifications
from ...permissions.permissionsid import get_permissions_id
from ...plugins.models import PluginDataModel
from ..avatars import store as avatars_store, delete_avatar
from ..enums import DefaultGroupId
from ..signatures import is_user_signature_valid
from ..utils import hash_email
from .group import Group
from .online import Online
from .rank import Rank


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("User must have an username.")
        if not email:
            raise ValueError("User must have an email address.")

        if not extra_fields.get("rank"):
            extra_fields["rank"] = Rank.objects.get_default()

        if (
            extra_fields.get("group")
            and extra_fields.get("group_id")
            and extra_fields.get("group").id != extra_fields.get("group_id")
        ):
            raise ValueError(
                "'group' and 'group_id' arguments can't be used simultaneously."
            )

        if extra_fields.get("group"):
            extra_fields["group_id"] = extra_fields.pop("group").id
        elif not extra_fields.get("group_id"):
            # Find default group's ID in database or fall back to the hardcoded one
            extra_fields["group_id"] = (
                Group.objects.filter(is_default=True)
                .values_list("id", flat=True)
                .first()
            ) or DefaultGroupId.MEMBERS

        if extra_fields.get("secondary_groups") and extra_fields.get(
            "secondary_groups_ids"
        ):
            raise ValueError(
                "'secondary_groups' and 'secondary_groups_ids' arguments can't be "
                "used simultaneously."
            )

        if extra_fields.get("groups_id"):
            raise ValueError(
                "'groups_id' value is calculated from 'group' and 'secondary_groups' "
                "and can't be set as an argument."
            )
        if extra_fields.get("permissions_id"):
            raise ValueError(
                "'permissions_id' value is calculated from user's groups and can't be "
                "set as an argument."
            )

        secondary_groups = extra_fields.pop("secondary_groups", None)
        secondary_groups_ids = extra_fields.pop("secondary_groups_ids", None)

        groups_ids = [extra_fields["group_id"]]
        if secondary_groups:
            groups_ids += [group.id for group in secondary_groups]
        elif secondary_groups_ids:
            groups_ids += secondary_groups_ids

        extra_fields["groups_ids"] = sorted(set(groups_ids))
        extra_fields["permissions_id"] = get_permissions_id(extra_fields["groups_ids"])

        user = self.model(**extra_fields)
        user.set_username(username)
        user.set_email(email)
        user.set_password(password)

        now = extra_fields.get("joined_on", timezone.now())
        user.last_login = now
        user.joined_on = now

        user.save(using=self._db)
        self._assert_user_has_authenticated_role(user)

        Online.objects.create(user=user, last_click=now)

        return user

    def _assert_user_has_authenticated_role(self, user):
        authenticated_role = Role.objects.get(special_role="authenticated")
        if authenticated_role not in user.roles.all():
            user.roles.add(authenticated_role)
        user.update_acl_key()
        user.save(update_fields=["acl_key"])

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_misago_root", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_misago_root", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_misago_root") is not True:
            raise ValueError("Superuser must have is_misago_root=True.")

        try:
            if not extra_fields.get("rank"):
                forum_team_rank = Rank.objects.get(
                    name=pgettext("default rank", "Forum team")
                )

                if forum_team_rank:
                    extra_fields["rank"] = forum_team_rank
        except Rank.DoesNotExist:
            pass

        if not extra_fields.get("group_id"):
            extra_fields["group_id"] = DefaultGroupId.ADMINS.value

        return self._create_user(username, email, password, **extra_fields)

    def get_by_username(self, username):
        return self.get(slug=slugify(username))

    def get_by_email(self, email):
        return self.get(email_hash=hash_email(email))

    def get_by_username_or_email(self, login):
        if "@" in login:
            return self.get(email_hash=hash_email(login))
        return self.get(slug=slugify(login))


class User(AbstractBaseUser, PluginDataModel, PermissionsMixin):
    ACTIVATION_NONE = 0
    ACTIVATION_USER = 1
    ACTIVATION_ADMIN = 2

    LIMIT_INVITES_TO_NONE = 0
    LIMIT_INVITES_TO_FOLLOWED = 1
    LIMIT_INVITES_TO_NOBODY = 2

    LIMIT_INVITES_TO_CHOICES = [
        (
            LIMIT_INVITES_TO_NONE,
            pgettext_lazy("user default invites choice", "Everybody"),
        ),
        (
            LIMIT_INVITES_TO_FOLLOWED,
            pgettext_lazy("user default invites choice", "Users I follow"),
        ),
        (
            LIMIT_INVITES_TO_NOBODY,
            pgettext_lazy("user default invites choice", "Nobody"),
        ),
    ]

    # Note that "username" field is purely for shows.
    # When searching users by their names, always use lowercased string
    # and slug field instead that is normalized around DB engines
    # differences in case handling.
    username = models.CharField(max_length=30)
    slug = models.CharField(max_length=30, unique=True)

    # Misago stores user email in two fields:
    # "email" holds normalized email address
    # "email_hash" is lowercase hash of email address used to identify account
    # as well as enforcing on database level that no more than one user can be
    # using one email address
    email = models.EmailField(max_length=255, db_index=True)
    email_hash = models.CharField(max_length=32, unique=True)

    joined_on = models.DateTimeField(
        pgettext_lazy("user", "joined on"), default=timezone.now, db_index=True
    )
    joined_from_ip = models.GenericIPAddressField(null=True, blank=True)
    is_hiding_presence = models.BooleanField(default=False)

    rank = models.ForeignKey(
        "Rank", null=True, blank=True, on_delete=models.deletion.PROTECT
    )
    group = models.ForeignKey("misago_users.Group", on_delete=models.deletion.PROTECT)
    groups_ids = ArrayField(models.PositiveIntegerField(), default=list)
    permissions_id = models.CharField(max_length=12)

    # Misago's root admin status
    # Root admin can do everything in Misago's admin panel but has no power in
    # Django's admin panel.
    is_misago_root = models.BooleanField(default=False)

    title = models.CharField(max_length=255, null=True, blank=True)

    requires_activation = models.PositiveIntegerField(default=ACTIVATION_NONE)

    # Controls user access to the Django site (not used by Misago)
    # This field is hardcoded in Django's admin logic, so we can't delete it.
    is_staff = models.BooleanField(
        pgettext_lazy("user", "staff status"),
        default=False,
        help_text=pgettext_lazy(
            "user", "Designates whether the user can log into admin sites."
        ),
    )

    roles = models.ManyToManyField("misago_acl.Role")
    acl_key = models.CharField(max_length=12, null=True, blank=True)

    is_active = models.BooleanField(
        pgettext_lazy("user", "active"),
        db_index=True,
        default=True,
        help_text=pgettext_lazy(
            "user",
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
        ),
    )
    is_active_staff_message = models.TextField(null=True, blank=True)

    is_deleting_account = models.BooleanField(default=False)

    avatar_tmp = models.ImageField(
        max_length=255, upload_to=avatars_store.upload_to, null=True, blank=True
    )
    avatar_src = models.ImageField(
        max_length=255, upload_to=avatars_store.upload_to, null=True, blank=True
    )
    avatar_crop = models.CharField(max_length=255, null=True, blank=True)
    avatars = models.JSONField(null=True, blank=True)
    is_avatar_locked = models.BooleanField(default=False)
    avatar_lock_user_message = models.TextField(null=True, blank=True)
    avatar_lock_staff_message = models.TextField(null=True, blank=True)

    signature = models.TextField(null=True, blank=True)
    signature_parsed = models.TextField(null=True, blank=True)
    signature_checksum = models.CharField(max_length=64, null=True, blank=True)
    is_signature_locked = models.BooleanField(default=False)
    signature_lock_user_message = models.TextField(null=True, blank=True)
    signature_lock_staff_message = models.TextField(null=True, blank=True)

    followers = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)

    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False
    )
    blocks = models.ManyToManyField(
        "self", related_name="blocked_by", symmetrical=False
    )

    limits_private_thread_invites_to = models.PositiveIntegerField(
        default=LIMIT_INVITES_TO_NONE, choices=LIMIT_INVITES_TO_CHOICES
    )
    unread_private_threads = models.PositiveIntegerField(default=0)
    sync_unread_private_threads = models.BooleanField(default=False)

    unread_notifications = models.PositiveIntegerField(default=0)

    watch_started_threads = models.PositiveIntegerField(
        default=ThreadNotifications.SITE_AND_EMAIL,
        choices=ThreadNotifications.choices,
    )
    watch_replied_threads = models.PositiveIntegerField(
        default=ThreadNotifications.SITE_AND_EMAIL,
        choices=ThreadNotifications.choices,
    )
    watch_new_private_threads_by_followed = models.PositiveIntegerField(
        default=ThreadNotifications.SITE_AND_EMAIL,
        choices=ThreadNotifications.choices,
    )
    watch_new_private_threads_by_other_users = models.PositiveIntegerField(
        default=ThreadNotifications.SITE_AND_EMAIL,
        choices=ThreadNotifications.choices,
    )
    notify_new_private_threads_by_followed = models.PositiveIntegerField(
        default=ThreadNotifications.SITE_AND_EMAIL,
        choices=ThreadNotifications.choices,
    )
    notify_new_private_threads_by_other_users = models.PositiveIntegerField(
        default=ThreadNotifications.SITE_AND_EMAIL,
        choices=ThreadNotifications.choices,
    )

    threads = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0, db_index=True)

    last_posted_on = models.DateTimeField(null=True, blank=True)

    profile_fields = HStoreField(default=dict)
    agreements = ArrayField(models.PositiveIntegerField(), default=list)

    USERNAME_FIELD = "slug"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        indexes = [
            *PluginDataModel.Meta.indexes,
            models.Index(
                name="misago_user_is_staff_part",
                fields=["is_staff"],
                condition=Q(is_staff=True),
            ),
            models.Index(
                name="misago_user_requires_acti_part",
                fields=["requires_activation"],
                condition=Q(requires_activation__gt=0),
            ),
            models.Index(
                name="misago_user_is_deleting_a_part",
                fields=["is_deleting_account"],
                condition=Q(is_deleting_account=True),
            ),
            models.Index(
                name="misago_user_is_misago_root",
                fields=["is_misago_root"],
                condition=Q(is_misago_root=True),
            ),
            GinIndex(
                name="misago_user_groups_ids",
                fields=["groups_ids"],
            ),
        ]

    def clean(self):
        self.username = self.normalize_username(self.username)
        self.email = UserManager.normalize_email(self.email)

    def lock(self):
        """locks user in DB, shortcut for locking user model in views"""
        return User.objects.select_for_update().get(pk=self.pk)

    def delete(self, *args, **kwargs):
        if kwargs.pop("delete_content", False):
            self.delete_content()

        username = kwargs.pop("anonymous_username", None)
        if username:
            self.anonymize_data(username)
        else:
            raise ValueError("user.delete() requires 'anonymous_username' argument")

        delete_avatar(self)

        return super().delete(*args, **kwargs)

    def delete_content(self):
        from ..signals import delete_user_content

        delete_user_content.send(sender=self)

    def mark_for_delete(self):
        self.is_active = False
        self.is_deleting_account = True
        self.save(update_fields=["is_active", "is_deleting_account"])

    def anonymize_data(self, anonymous_username):
        """Replaces username with anonymized one, then send anonymization signal.

        Items associated with this user then anonymize their user-specific data
        like username or IP addresses.
        """
        self.username = anonymous_username
        self.slug = slugify(self.username)

        from ..signals import anonymize_user_data

        anonymize_user_data.send(sender=self)

    @property
    def is_misago_admin(self):
        return self.is_misago_root or DefaultGroupId.ADMINS in self.groups_ids

    @property
    def requires_activation_by_admin(self):
        return self.requires_activation == self.ACTIVATION_ADMIN

    @property
    def requires_activation_by_user(self):
        return self.requires_activation == self.ACTIVATION_USER

    @property
    def can_be_messaged_by_everyone(self):
        preference = self.limits_private_thread_invites_to
        return preference == self.LIMIT_INVITES_TO_NONE

    @property
    def can_be_messaged_by_followed(self):
        preference = self.limits_private_thread_invites_to
        return preference == self.LIMIT_INVITES_TO_FOLLOWED

    @property
    def can_be_messaged_by_nobody(self):
        preference = self.limits_private_thread_invites_to
        return preference == self.LIMIT_INVITES_TO_NOBODY

    @property
    def has_valid_signature(self):
        return is_user_signature_valid(self)

    def get_absolute_url(self):
        return reverse("misago:user", kwargs={"slug": self.slug, "pk": self.pk})

    def get_username(self):
        """dirty hack: return real username instead of normalized slug"""
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_real_name(self):
        # Bug: https://github.com/rafalp/Misago/issues/1352
        # On some very rare cases self.profile_fields is deserialized as string
        # by Django's ORM. I am unable to reproduce this, but in case when this
        # bug occurs, this code branch will print extra information about it
        if not isinstance(self.profile_fields, dict):
            from django.db import connections
            from django.db.backends.signals import connection_created
            from django.contrib.postgres.signals import get_hstore_oids

            receivers = ", ".join([str(r[1]()) for r in connection_created.receivers])
            dead_receivers = "TRUE" if connection_created._dead_receivers else "FALSE"

            valid_oids = None
            cached_oids = get_hstore_oids("default")

            with connections["default"].cursor() as cursor:
                cursor.execute(
                    "SELECT t.oid, typarray "
                    "FROM pg_type t "
                    "JOIN pg_namespace ns ON typnamespace = ns.oid "
                    "WHERE typname = 'hstore'"
                )
                oids = []
                array_oids = []
                for row in cursor:
                    oids.append(row[0])
                    array_oids.append(row[1])
                valid_oids = tuple(oids), tuple(array_oids)

            raise RuntimeError(
                f"'profile_fields' has wrong type! Please post this WHOLE message on https://github.com/rafalp/Misago/issues/1352 "
                f"OID: '{cached_oids}' (valid: '{valid_oids}') "
                f"Receivers: '{receivers}' (has dead: {dead_receivers}) "
                f"Repr: {repr(self.profile_fields)}"
            )

        return self.profile_fields.get("real_name")

    def set_username(self, new_username, changed_by=None):
        new_username = self.normalize_username(new_username)
        if new_username != self.username:
            old_username = self.username
            self.username = new_username
            self.slug = slugify(new_username)

            if self.pk:
                changed_by = changed_by or self
                namechange = self.record_name_change(
                    changed_by, new_username, old_username
                )

                from ..signals import username_changed

                username_changed.send(sender=self)

                return namechange

    def record_name_change(self, changed_by, new_username, old_username):
        return self.namechanges.create(
            new_username=new_username,
            old_username=old_username,
            changed_by=changed_by,
            changed_by_username=changed_by.username,
        )

    def set_email(self, new_email):
        self.email = UserManager.normalize_email(new_email)
        self.email_hash = hash_email(new_email)

    def set_groups(self, group: Group, secondary_groups: list[Group] | None = None):
        self.group = group
        groups_ids = [group.id]
        if secondary_groups:
            groups_ids += [secondary_group.id for secondary_group in secondary_groups]

        self.groups_ids = sorted(set(groups_ids))
        self.permissions_id = get_permissions_id(self.groups_ids)

    def get_any_title(self):
        if self.title:
            return self.title

        if self.rank.title:
            return self.rank.title

        return str(self.rank)

    def get_roles(self):
        roles_pks = []
        roles_dict = {}

        for role in self.roles.all():
            roles_pks.append(role.pk)
            role.origin = self
            roles_dict[role.pk] = role

        if self.rank:
            for role in self.rank.roles.all():
                if role.pk not in roles_pks:
                    role.origin = self.rank
                    roles_pks.append(role.pk)
                    roles_dict[role.pk] = role

        return [roles_dict[r] for r in sorted(roles_pks)]

    def update_acl_key(self):
        roles_pks = []
        for role in self.get_roles():
            if role.origin == "self":
                roles_pks.append("u%s" % role.pk)
            else:
                roles_pks.append("%s:%s" % (self.rank.pk, role.pk))

        self.acl_key = md5(",".join(roles_pks).encode()).hexdigest()[:12]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """sends an email to this user (for compat with Django)"""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_following(self, user_or_id: Union["User", int]) -> bool:
        if isinstance(user_or_id, int):
            user_id = user_or_id
        elif isinstance(user_or_id, User):
            user_id = user_or_id.id
        else:
            raise ValueError("'user_or_id' argument must be an int or User instance")

        return self.follows.filter(id=user_id).exists()

    def is_blocking(self, user_or_id: Union["User", int]) -> bool:
        if isinstance(user_or_id, int):
            user_id = user_or_id
        elif isinstance(user_or_id, User):
            user_id = user_or_id.id
        else:
            raise ValueError("'user_or_id' argument must be an int or User instance")

        return self.blocks.filter(id=user_id).exists()

    def get_unread_notifications_for_display(self) -> Optional[str]:
        if not self.unread_notifications:
            return None

        if self.unread_notifications > settings.MISAGO_UNREAD_NOTIFICATIONS_LIMIT:
            return f"{settings.MISAGO_UNREAD_NOTIFICATIONS_LIMIT}+"

        return str(self.unread_notifications)

    def clear_unread_private_threads(self):
        if self.unread_private_threads or self.sync_unread_private_threads:
            self.unread_private_threads = 0
            self.sync_unread_private_threads = False
            self.save(
                update_fields=["unread_private_threads", "sync_unread_private_threads"]
            )


class UsernameChange(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="namechanges", on_delete=models.CASCADE
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="user_renames",
        on_delete=models.SET_NULL,
    )
    changed_by_username = models.CharField(max_length=30)
    changed_on = models.DateTimeField(default=timezone.now)
    new_username = models.CharField(max_length=255)
    old_username = models.CharField(max_length=255)

    class Meta:
        get_latest_by = "changed_on"

    def set_change_author(self, user):
        self.changed_by = user
        self.changed_by_username = user.username


class AnonymousUser(DjangoAnonymousUser):
    is_misago_admin = False
    is_misago_root = False
    acl_key = "anonymous"

    @property
    def acl_cache(self):
        raise Exception("AnonymousUser.acl_cache has been removed")

    @acl_cache.setter
    def acl_cache(self, value):
        raise TypeError("AnonymousUser instances can't be made ACL aware")

    def get_roles(self):
        try:
            return [Role.objects.get(special_role="anonymous")]
        except Role.DoesNotExist:
            raise RuntimeError("Anonymous user role not found.")

    def update_acl_key(self):
        raise TypeError("Can't update ACL key on anonymous users")
