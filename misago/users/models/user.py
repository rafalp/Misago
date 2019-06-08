from hashlib import md5

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.postgres.fields import ArrayField, HStoreField, JSONField
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .. import avatars
from ...acl.models import Role
from ...conf import settings
from ...core.utils import slugify
from ..signatures import is_user_signature_valid
from ..utils import hash_email
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
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        try:
            if not extra_fields.get("rank"):
                extra_fields["rank"] = Rank.objects.get(name=_("Forum team"))
        except Rank.DoesNotExist:
            pass

        return self._create_user(username, email, password, **extra_fields)

    def get_by_username(self, username):
        return self.get(slug=slugify(username))

    def get_by_email(self, email):
        return self.get(email_hash=hash_email(email))

    def get_by_username_or_email(self, login):
        if "@" in login:
            return self.get(email_hash=hash_email(login))
        return self.get(slug=slugify(login))


class User(AbstractBaseUser, PermissionsMixin):
    ACTIVATION_NONE = 0
    ACTIVATION_USER = 1
    ACTIVATION_ADMIN = 2

    SUBSCRIPTION_NONE = 0
    SUBSCRIPTION_NOTIFY = 1
    SUBSCRIPTION_ALL = 2

    SUBSCRIPTION_CHOICES = [
        (SUBSCRIPTION_NONE, _("No")),
        (SUBSCRIPTION_NOTIFY, _("Notify")),
        (SUBSCRIPTION_ALL, _("Notify with e-mail")),
    ]

    LIMIT_INVITES_TO_NONE = 0
    LIMIT_INVITES_TO_FOLLOWED = 1
    LIMIT_INVITES_TO_NOBODY = 2

    LIMIT_INVITES_TO_CHOICES = [
        (LIMIT_INVITES_TO_NONE, _("Everybody")),
        (LIMIT_INVITES_TO_FOLLOWED, _("Users I follow")),
        (LIMIT_INVITES_TO_NOBODY, _("Nobody")),
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
        _("joined on"), default=timezone.now, db_index=True
    )
    joined_from_ip = models.GenericIPAddressField(null=True, blank=True)
    is_hiding_presence = models.BooleanField(default=False)

    rank = models.ForeignKey(
        "Rank", null=True, blank=True, on_delete=models.deletion.PROTECT
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    requires_activation = models.PositiveIntegerField(default=ACTIVATION_NONE)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into admin sites."),
    )

    roles = models.ManyToManyField("misago_acl.Role")
    acl_key = models.CharField(max_length=12, null=True, blank=True)

    is_active = models.BooleanField(
        _("active"),
        db_index=True,
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_active_staff_message = models.TextField(null=True, blank=True)

    is_deleting_account = models.BooleanField(default=False)

    avatar_tmp = models.ImageField(
        max_length=255, upload_to=avatars.store.upload_to, null=True, blank=True
    )
    avatar_src = models.ImageField(
        max_length=255, upload_to=avatars.store.upload_to, null=True, blank=True
    )
    avatar_crop = models.CharField(max_length=255, null=True, blank=True)
    avatars = JSONField(null=True, blank=True)
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

    subscribe_to_started_threads = models.PositiveIntegerField(
        default=SUBSCRIPTION_NONE, choices=SUBSCRIPTION_CHOICES
    )
    subscribe_to_replied_threads = models.PositiveIntegerField(
        default=SUBSCRIPTION_NONE, choices=SUBSCRIPTION_CHOICES
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

        avatars.delete_avatar(self)

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

    def get_any_title(self):
        return self.title or self.rank.title or self.rank.name

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

    def is_following(self, user_or_id):
        try:
            user_id = user_or_id.id
        except AttributeError:
            user_id = user_or_id

        try:
            self.follows.get(id=user_id)
            return True
        except User.DoesNotExist:
            return False

    def is_blocking(self, user_or_id):
        try:
            user_id = user_or_id.id
        except AttributeError:
            user_id = user_or_id

        try:
            self.blocks.get(id=user_id)
            return True
        except User.DoesNotExist:
            return False


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
