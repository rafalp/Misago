from hashlib import md5

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager as BaseUserManager,
                                        AnonymousUser as DjangoAnonymousUser)
from django.core.mail import send_mail
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.acl import get_user_acl
from misago.acl.models import Role
from misago.conf import settings
from misago.core.utils import slugify

from misago.users.models.rank import Rank
from misago.users.utils import hash_email


__all__ = [
    'ACTIVATION_REQUIRED_NONE', 'ACTIVATION_REQUIRED_USER',
    'ACTIVATION_REQUIRED_ADMIN', 'PRESENCE_VISIBILITY_ALL',
    'PRESENCE_VISIBILITY_FOLLOWED', 'PRESENCE_VISIBILITY_ALLOWED',
    'PRESENCE_VISIBILITY_CHOICES', 'AUTO_SUBSCRIBE_NONE',
    'AUTO_SUBSCRIBE_WATCH', 'AUTO_SUBSCRIBE_WATCH_AND_EMAIL',
    'AUTO_SUBSCRIBE_CHOICES', 'AnonymousUser', 'User', 'Online',
]


ACTIVATION_REQUIRED_NONE = 0
ACTIVATION_REQUIRED_USER = 1
ACTIVATION_REQUIRED_ADMIN = 2


PRESENCE_VISIBILITY_ALL = 0
PRESENCE_VISIBILITY_FOLLOWED = 1
PRESENCE_VISIBILITY_ALLOWED = 2

PRESENCE_VISIBILITY_CHOICES = (
    (PRESENCE_VISIBILITY_ALL, _("Everyone")),
    (PRESENCE_VISIBILITY_FOLLOWED, _("Users I follow")),
    (PRESENCE_VISIBILITY_ALLOWED, _("Users with permission"))
)


AUTO_SUBSCRIBE_NONE = 0
AUTO_SUBSCRIBE_WATCH = 1
AUTO_SUBSCRIBE_WATCH_AND_EMAIL = 2

AUTO_SUBSCRIBE_CHOICES = (
    (AUTO_SUBSCRIBE_NONE, _("Do nothing.")),
    (AUTO_SUBSCRIBE_WATCH, _("Add to watched list.")),
    (AUTO_SUBSCRIBE_WATCH_AND_EMAIL,
     _("Add to watched list with e-mail notification."))
)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        from misago.users.validators import (validate_email, validate_password,
                                             validate_username)

        with transaction.atomic():
            if not email:
                raise ValueError(_("User must have an email address."))
            if not password:
                raise ValueError(_("User must have a password."))

            validate_username(username)
            validate_email(email)
            validate_password(password)

            if not 'joined_from_ip' in extra_fields:
                extra_fields['joined_from_ip'] = '127.0.0.1'

            if not 'timezone' in extra_fields:
                extra_fields['timezone'] = settings.default_timezone

            WATCH_DICT = {
                'no': AUTO_SUBSCRIBE_NONE,
                'watch': AUTO_SUBSCRIBE_WATCH,
                'watch_email': AUTO_SUBSCRIBE_WATCH_AND_EMAIL,
            }

            if not 'subscribe_to_started_threads' in extra_fields:
                new_value = WATCH_DICT[settings.subscribe_start]
                extra_fields['subscribe_to_started_threads'] = new_value

            if not 'subscribe_to_replied_threads' in extra_fields:
                new_value = WATCH_DICT[settings.subscribe_reply]
                extra_fields['subscribe_to_replied_threads'] = new_value

            now = timezone.now()
            user = self.model(is_staff=False, is_superuser=False, last_login=now,
                              joined_on=now, **extra_fields)

            user.set_username(username)
            user.set_email(email)
            user.set_password(password)

            if not 'rank' in extra_fields:
                user.rank = Rank.objects.get_default()

            user.save(using=self._db)

            authenticated_role = Role.objects.get(special_role='authenticated')
            if authenticated_role not in user.roles.all():
                user.roles.add(authenticated_role)

            user.update_acl_key()
            user.save(update_fields=['acl_key'])

            return user

    def create_superuser(self, username, email, password):
        with transaction.atomic():
            user = self.create_user(username, email, password=password)

            try:
                user.rank = Rank.objects.get(name=_("Forum Team"))
                user.update_acl_key()
            except Rank.DoesNotExist:
                pass

            user.is_staff = True
            user.is_superuser = True
            user.save(update_fields=['is_staff', 'is_superuser'], using=self._db)
            return user

    def get_by_username(self, username):
        return self.get(username_slug=slugify(username))

    def get_by_email(self, email):
        return self.get(email_hash=hash_email(email))

    def get_by_username_or_email(self, login):
        queryset = models.Q(username_slug=slugify(login))
        queryset = queryset | models.Q(email_hash=hash_email(login))
        return self.get(queryset)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Note that "username" field is purely for shows.
    When searching users by their names, always use lowercased string
    and username_slug field instead that is normalized around DB engines
    differences in case handling.
    """
    username = models.CharField(max_length=30)
    username_slug = models.CharField(max_length=30, unique=True)
    """
    Misago stores user email in two fields:
    "email" holds normalized email address
    "email_hash" is lowercase hash of email address used to identify account
    as well as enforcing on database level that no more than one user can be
    using one email address
    """
    email = models.EmailField(max_length=255, db_index=True)
    email_hash = models.CharField(max_length=32, unique=True)
    joined_on = models.DateTimeField(_('joined on'), default=timezone.now)
    joined_from_ip = models.GenericIPAddressField()
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    presence_visibility = models.PositiveIntegerField(
        default=PRESENCE_VISIBILITY_ALL)

    timezone = models.CharField(max_length=255, default='utc')

    rank = models.ForeignKey(
        'Rank', null=True, blank=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, null=True, blank=True)
    requires_activation = models.PositiveIntegerField(
        default=ACTIVATION_REQUIRED_NONE)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into admin sites.'))
    roles = models.ManyToManyField('misago_acl.Role')
    acl_key = models.CharField(max_length=12, null=True, blank=True)

    is_avatar_banned = models.BooleanField(default=False)
    avatar_type = models.CharField(max_length=10, null=True, blank=True)
    avatar_image = models.CharField(max_length=255, null=True, blank=True)
    avatar_original = models.CharField(max_length=255, null=True, blank=True)
    avatar_temp = models.CharField(max_length=255, null=True, blank=True)
    avatar_crop = models.CharField(max_length=255, null=True, blank=True)
    avatar_ban_user_message = models.TextField(null=True, blank=True)
    avatar_ban_staff_message = models.TextField(null=True, blank=True)

    is_signature_banned = models.BooleanField(default=False)
    signature = models.TextField(null=True, blank=True)
    signature_preparsed = models.TextField(null=True, blank=True)
    signature_ban_user_message = models.TextField(null=True, blank=True)
    signature_ban_staff_message = models.TextField(null=True, blank=True)

    warning_level = models.PositiveIntegerField(default=0)
    warning_level_update_on = models.DateTimeField(null=True, blank=True)

    following = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)

    new_alerts = models.PositiveIntegerField(default=0)

    limit_private_thread_invites = models.PositiveIntegerField(default=0)
    unread_private_threads = models.PositiveIntegerField(default=0)
    sync_unred_private_threads = models.BooleanField(default=False)

    subscribe_to_started_threads = models.PositiveIntegerField(
        default=AUTO_SUBSCRIBE_NONE)
    subscribe_to_replied_threads = models.PositiveIntegerField(
        default=AUTO_SUBSCRIBE_NONE)

    threads = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)

    last_post = models.DateTimeField(null=True, blank=True)
    last_search = models.DateTimeField(null=True, blank=True)

    is_active = True # Django's is_active means "is not deleted"

    USERNAME_FIELD = 'username_slug'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    @property
    def acl(self):
        try:
            return self._acl_cache
        except AttributeError:
            self._acl_cache = get_user_acl(self)
            return self._acl_cache

    @acl.setter
    def acl(self, value):
        raise TypeError('Cannot make User instances ACL aware')

    @property
    def requires_activation_by_admin(self):
        return self.requires_activation == ACTIVATION_REQUIRED_ADMIN

    @property
    def requires_activation_by_user(self):
        return self.requires_activation == ACTIVATION_REQUIRED_USER

    @property
    def staff_level(self):
        if self.is_superuser:
            return 2
        elif self.is_staff:
            return 1
        else:
            return 0

    @staff_level.setter
    def staff_level(self, new_level):
        if new_level == 2:
            self.is_superuser = True
            self.is_staff = True
        elif new_level == 1:
            self.is_superuser = False
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False

    def get_username(self):
        """
        Dirty hack: return real username instead of normalized slug
        """
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def set_username(self, new_username):
        self.username = new_username
        self.username_slug = slugify(new_username)

    def set_email(self, new_email):
        self.email = UserManager.normalize_email(new_email)
        self.email_hash = hash_email(new_email)

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

        self.acl_key = md5(','.join(roles_pks)).hexdigest()[:12]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Online(models.Model):
    user = models.OneToOneField(User, primary_key=True,
                                related_name='online_tracker')
    current_ip = models.GenericIPAddressField()
    last_click = models.DateTimeField(default=timezone.now)


class AnonymousUser(DjangoAnonymousUser):
    acl_key = 'anonymous'

    @property
    def acl(self):
        try:
            return self._acl_cache
        except AttributeError:
            self._acl_cache = get_user_acl(self)
            return self._acl_cache

    @acl.setter
    def acl(self, value):
        raise TypeError('Cannot make AnonymousUser instances ACL aware')

    def get_roles(self):
        try:
            return [Role.objects.get(special_role="anonymous")]
        except Role.DoesNotExist:
            raise RuntimeError("Anonymous user role not found.")

    def update_acl_key(self):
        raise TypeError("Can't update ACL key on anonymous users")
