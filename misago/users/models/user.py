from hashlib import md5

from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.contrib.postgres.fields import JSONField
from django.core.mail import send_mail
from django.db import IntegrityError, models, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.acl import get_user_acl
from misago.acl.models import Role
from misago.conf import settings
from misago.core.pgutils import PgPartialIndex
from misago.core.utils import slugify
from misago.users import avatars
from misago.users.signatures import is_user_signature_valid
from misago.users.utils import hash_email

from .rank import Rank


class UserManager(BaseUserManager):
    @transaction.atomic
    def create_user(
            self, username, email, password=None, set_default_avatar=False, **extra_fields
    ):
        from misago.users.validators import validate_email, validate_username

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)

        if not email:
            raise ValueError(_("User must have an email address."))
        if not password:
            raise ValueError(_("User must have a password."))

        if not 'joined_from_ip' in extra_fields:
            extra_fields['joined_from_ip'] = '127.0.0.1'

        WATCH_DICT = {
            'no': self.model.SUBSCRIBE_NONE,
            'watch': self.model.SUBSCRIBE_NOTIFY,
            'watch_email': self.model.SUBSCRIBE_ALL,
        }

        if not 'subscribe_to_started_threads' in extra_fields:
            new_value = WATCH_DICT[settings.subscribe_start]
            extra_fields['subscribe_to_started_threads'] = new_value

        if not 'subscribe_to_replied_threads' in extra_fields:
            new_value = WATCH_DICT[settings.subscribe_reply]
            extra_fields['subscribe_to_replied_threads'] = new_value

        extra_fields.update({'is_staff': False, 'is_superuser': False})

        now = timezone.now()
        user = self.model(last_login=now, joined_on=now, **extra_fields)

        user.set_username(username)
        user.set_email(email)
        user.set_password(password)

        validate_username(username)
        validate_email(email)
        validate_password(password, user=user)

        if not 'rank' in extra_fields:
            user.rank = Rank.objects.get_default()

        user.save(using=self._db)

        if set_default_avatar:
            avatars.set_default_avatar(
                user, settings.default_avatar, settings.default_gravatar_fallback
            )
        else:
            # just for test purposes
            user.avatars = [{'size': 400, 'url': '/placekitten.com/400/400'}]

        authenticated_role = Role.objects.get(special_role='authenticated')
        if authenticated_role not in user.roles.all():
            user.roles.add(authenticated_role)
        user.update_acl_key()

        user.save(update_fields=['avatars', 'acl_key'])

        # populate online tracker with default value
        Online.objects.create(
            user=user,
            current_ip=extra_fields['joined_from_ip'],
            last_click=now,
        )

        return user

    @transaction.atomic
    def create_superuser(self, username, email, password, set_default_avatar=False):
        user = self.create_user(
            username,
            email,
            password=password,
            set_default_avatar=set_default_avatar,
        )

        try:
            user.rank = Rank.objects.get(name=_("Forum team"))
            user.update_acl_key()
        except Rank.DoesNotExist:
            pass

        user.is_staff = True
        user.is_superuser = True

        updated_fields = ('rank', 'acl_key', 'is_staff', 'is_superuser')
        user.save(update_fields=updated_fields, using=self._db)
        return user

    def get_by_username(self, username):
        return self.get(slug=slugify(username))

    def get_by_email(self, email):
        return self.get(email_hash=hash_email(email))

    def get_by_username_or_email(self, login):
        queryset = models.Q(slug=slugify(login))
        queryset = queryset | models.Q(email_hash=hash_email(login))
        return self.get(queryset)


class User(AbstractBaseUser, PermissionsMixin):
    ACTIVATION_NONE = 0
    ACTIVATION_USER = 1
    ACTIVATION_ADMIN = 2

    SUBSCRIBE_NONE = 0
    SUBSCRIBE_NOTIFY = 1
    SUBSCRIBE_ALL = 2

    SUBSCRIBE_CHOICES = [
        (SUBSCRIBE_NONE, _("No")),
        (SUBSCRIBE_NOTIFY, _("Notify")),
        (SUBSCRIBE_ALL, _("Notify with e-mail")),
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

    joined_on = models.DateTimeField(_('joined on'), default=timezone.now)
    joined_from_ip = models.GenericIPAddressField()
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    is_hiding_presence = models.BooleanField(default=False)

    rank = models.ForeignKey(
        'Rank',
        null=True,
        blank=True,
        on_delete=models.deletion.PROTECT,
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    requires_activation = models.PositiveIntegerField(default=ACTIVATION_NONE)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into admin sites.'),
    )

    roles = models.ManyToManyField('misago_acl.Role')
    acl_key = models.CharField(max_length=12, null=True, blank=True)

    is_active = models.BooleanField(
        _('active'),
        db_index=True,
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_active_staff_message = models.TextField(null=True, blank=True)

    avatar_tmp = models.ImageField(
        max_length=255,
        upload_to=avatars.store.upload_to,
        null=True,
        blank=True,
    )
    avatar_src = models.ImageField(
        max_length=255,
        upload_to=avatars.store.upload_to,
        null=True,
        blank=True,
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
        'self',
        related_name='followed_by',
        symmetrical=False,
    )
    blocks = models.ManyToManyField(
        'self',
        related_name='blocked_by',
        symmetrical=False,
    )

    limits_private_thread_invites_to = models.PositiveIntegerField(
        default=LIMIT_INVITES_TO_NONE,
        choices=LIMIT_INVITES_TO_CHOICES,
    )
    unread_private_threads = models.PositiveIntegerField(default=0)
    sync_unread_private_threads = models.BooleanField(default=False)

    subscribe_to_started_threads = models.PositiveIntegerField(
        default=SUBSCRIBE_NONE,
        choices=SUBSCRIBE_CHOICES,
    )
    subscribe_to_replied_threads = models.PositiveIntegerField(
        default=SUBSCRIBE_NONE,
        choices=SUBSCRIBE_CHOICES,
    )

    threads = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0, db_index=True)

    last_posted_on = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'slug'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        indexes = [
            PgPartialIndex(
                fields=['is_staff'],
                where={'is_staff': True},
            ),
            PgPartialIndex(
                fields=['requires_activation'],
                where={'requires_activation__gt': 0},
            ),
        ]

    def clean(self):
        self.username = self.normalize_username(self.username)
        self.email = UserManager.normalize_email(self.email)

    def lock(self):
        """locks user in DB, shortcut for locking user model in views"""
        return User.objects.select_for_update().get(pk=self.pk)

    def delete(self, *args, **kwargs):
        if kwargs.pop('delete_content', False):
            self.delete_content()

        avatars.delete_avatar(self)

        return super(User, self).delete(*args, **kwargs)

    def delete_content(self):
        from misago.users.signals import delete_user_content
        delete_user_content.send(sender=self)

    @property
    def acl_cache(self):
        try:
            return self._acl_cache
        except AttributeError:
            self._acl_cache = get_user_acl(self)
            return self._acl_cache

    @acl_cache.setter
    def acl_cache(self, value):
        raise TypeError("acl_cache can't be assigned")

    @property
    def acl_(self):
        raise NotImplementedError('user.acl_ property was renamed to user.acl')

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
        return reverse(
            'misago:user', kwargs={
                'slug': self.slug,
                'pk': self.pk,
            }
        )

    def get_username(self):
        """dirty hack: return real username instead of normalized slug"""
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def set_username(self, new_username, changed_by=None):
        new_username = self.normalize_username(new_username)
        if new_username != self.username:
            old_username = self.username
            self.username = new_username
            self.slug = slugify(new_username)

            if self.pk:
                changed_by = changed_by or self
                self.record_name_change(changed_by, new_username, old_username)

                from misago.users.signals import username_changed
                username_changed.send(sender=self)

    def record_name_change(self, changed_by, new_username, old_username):
        self.namechanges.create(
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
            if role.origin == 'self':
                roles_pks.append('u%s' % role.pk)
            else:
                roles_pks.append('%s:%s' % (self.rank.pk, role.pk))

        self.acl_key = md5(','.join(roles_pks).encode()).hexdigest()[:12]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """sends an email to this user (for compat with Django)"""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_following(self, user):
        try:
            self.follows.get(pk=user.pk)
            return True
        except User.DoesNotExist:
            return False

    def is_blocking(self, user):
        try:
            self.blocks.get(pk=user.pk)
            return True
        except User.DoesNotExist:
            return False


class Online(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        related_name='online_tracker',
        on_delete=models.CASCADE,
    )
    current_ip = models.GenericIPAddressField()
    last_click = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        try:
            super(Online, self).save(*args, **kwargs)
        except IntegrityError:
            pass  # first come is first serve in online tracker


class UsernameChange(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='namechanges',
        on_delete=models.CASCADE,
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='user_renames',
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
    acl_key = 'anonymous'

    @property
    def acl_cache(self):
        try:
            return self._acl_cache
        except AttributeError:
            self._acl_cache = get_user_acl(self)
            return self._acl_cache

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
