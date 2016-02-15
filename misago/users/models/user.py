from hashlib import md5

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager as BaseUserManager,
                                        AnonymousUser as DjangoAnonymousUser)
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError, models, transaction
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.acl import get_user_acl
from misago.acl.models import Role
from misago.conf import settings
from misago.core.utils import slugify

from misago.users.models.rank import Rank
from misago.users import avatars
from misago.users.signatures import (is_user_signature_valid,
                                     make_signature_checksum)
from misago.users.utils import hash_email


__all__ = [
    'ACTIVATION_REQUIRED_NONE',
    'ACTIVATION_REQUIRED_USER',
    'ACTIVATION_REQUIRED_ADMIN',
    'AUTO_SUBSCRIBE_NONE',
    'AUTO_SUBSCRIBE_WATCH',
    'AUTO_SUBSCRIBE_WATCH_AND_EMAIL',
    'AUTO_SUBSCRIBE_CHOICES',
    'LIMITS_PRIVATE_THREAD_INVITES_TO_NONE',
    'LIMITS_PRIVATE_THREAD_INVITES_TO_FOLLOWED',
    'LIMITS_PRIVATE_THREAD_INVITES_TO_NOBODY',
    'PRIVATE_THREAD_INVITES_LIMITS_CHOICES',
    'AnonymousUser', 'User', 'UsernameChange', 'Online',
]


ACTIVATION_REQUIRED_NONE = 0
ACTIVATION_REQUIRED_USER = 1
ACTIVATION_REQUIRED_ADMIN = 2


AUTO_SUBSCRIBE_NONE = 0
AUTO_SUBSCRIBE_WATCH = 1
AUTO_SUBSCRIBE_WATCH_AND_EMAIL = 2

AUTO_SUBSCRIBE_CHOICES = (
    (AUTO_SUBSCRIBE_NONE, _("Do nothing")),
    (AUTO_SUBSCRIBE_WATCH, _("Bookmark")),
    (AUTO_SUBSCRIBE_WATCH_AND_EMAIL,
     _("Bookmark with e-mail notification"))
)


LIMITS_PRIVATE_THREAD_INVITES_TO_NONE = 0
LIMITS_PRIVATE_THREAD_INVITES_TO_FOLLOWED = 1
LIMITS_PRIVATE_THREAD_INVITES_TO_NOBODY = 2

PRIVATE_THREAD_INVITES_LIMITS_CHOICES = (
    (LIMITS_PRIVATE_THREAD_INVITES_TO_NONE, _("Everybody")),
    (LIMITS_PRIVATE_THREAD_INVITES_TO_FOLLOWED, _("Users I follow")),
    (LIMITS_PRIVATE_THREAD_INVITES_TO_NOBODY, _("Nobody")),
)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None,
                    set_default_avatar=False, **extra_fields):
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
            user = self.model(is_staff=False, is_superuser=False,
                              last_login=now, joined_on=now, **extra_fields)

            user.set_username(username)
            user.set_email(email)
            user.set_password(password)

            if not 'rank' in extra_fields:
                user.rank = Rank.objects.get_default()

            user.save(using=self._db)

            if set_default_avatar:
                avatars.set_default_avatar(user)
                user.avatar_hash = avatars.get_avatar_hash(user)
            else:
                user.avatar_hash = 'abcdef01'

            authenticated_role = Role.objects.get(special_role='authenticated')
            if authenticated_role not in user.roles.all():
                user.roles.add(authenticated_role)
            user.update_acl_key()

            user.save(update_fields=['avatar_hash', 'acl_key'])

            return user

    def create_superuser(self, username, email, password,
                         set_default_avatar=False):
        with transaction.atomic():
            user = self.create_user(username, email, password=password,
                                    set_default_avatar=set_default_avatar)

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
    """
    Note that "username" field is purely for shows.
    When searching users by their names, always use lowercased string
    and slug field instead that is normalized around DB engines
    differences in case handling.
    """
    username = models.CharField(max_length=30)
    slug = models.CharField(max_length=30, unique=True)
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
    is_hiding_presence = models.BooleanField(default=False)

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

    is_avatar_locked = models.BooleanField(default=False)
    avatar_hash = models.CharField(max_length=8)
    avatar_crop = models.CharField(max_length=255, null=True, blank=True)
    avatar_lock_user_message = models.TextField(null=True, blank=True)
    avatar_lock_staff_message = models.TextField(null=True, blank=True)

    is_signature_locked = models.BooleanField(default=False)
    signature = models.TextField(null=True, blank=True)
    signature_parsed = models.TextField(null=True, blank=True)
    signature_checksum = models.CharField(max_length=64, null=True, blank=True)
    signature_lock_user_message = models.TextField(null=True, blank=True)
    signature_lock_staff_message = models.TextField(null=True, blank=True)

    warning_level = models.PositiveIntegerField(default=0)
    warning_level_update_on = models.DateTimeField(null=True, blank=True)

    followers = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)

    follows = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False)
    blocks = models.ManyToManyField(
        'self', related_name='blocked_by', symmetrical=False)

    new_notifications = models.PositiveIntegerField(default=0)

    limits_private_thread_invites_to = models.PositiveIntegerField(
        default=LIMITS_PRIVATE_THREAD_INVITES_TO_NONE)
    unread_private_threads = models.PositiveIntegerField(default=0)
    sync_unread_private_threads = models.BooleanField(default=False)

    subscribe_to_started_threads = models.PositiveIntegerField(
        default=AUTO_SUBSCRIBE_NONE)
    subscribe_to_replied_threads = models.PositiveIntegerField(
        default=AUTO_SUBSCRIBE_NONE)

    threads = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0, db_index=True)

    last_posted_on = models.DateTimeField(null=True, blank=True)
    last_searched_on = models.DateTimeField(null=True, blank=True)

    reads_cutoff = models.DateTimeField(default=timezone.now)
    new_threads_cutoff = models.DateTimeField(default=timezone.now)
    unread_threads_cutoff = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'slug'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def lock(self):
        """Locks user in DB"""
        return User.objects.select_for_update().get(id=self.id)

    def delete(self, *args, **kwargs):
        if kwargs.pop('delete_content', False):
            self.delete_content()

        avatars.delete_avatar(self)

        return super(User, self).delete(*args, **kwargs)

    def delete_content(self):
        from misago.users.signals import delete_user_content
        delete_user_content.send(sender=self)

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
    def full_title(self):
        return self.title or self.rank.name

    @property
    def short_title(self):
        return self.title or self.rank.title

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

    @property
    def can_be_messaged_by_everyone(self):
        preference = self.limits_private_thread_invites_to
        return preference == LIMITS_PRIVATE_THREAD_INVITES_TO_NONE

    @property
    def can_be_messaged_by_followed(self):
        preference = self.limits_private_thread_invites_to
        return preference == LIMITS_PRIVATE_THREAD_INVITES_TO_FOLLOWED

    @property
    def can_be_messaged_by_nobody(self):
        preference = self.limits_private_thread_invites_to
        return preference == LIMITS_PRIVATE_THREAD_INVITES_TO_NOBODY

    @property
    def has_valid_signature(self):
        return is_user_signature_valid(self)

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

    def get_absolute_url(self):
        return reverse('misago:user', kwargs={
            'user_slug': self.slug,
            'user_id': self.id,
        })

    def get_username(self):
        """
        Dirty hack: return real username instead of normalized slug
        """
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def set_username(self, new_username, changed_by=None):
        if new_username != self.username:
            old_username = self.username
            self.username = new_username
            self.slug = slugify(new_username)

            if self.pk:
                changed_by = changed_by or self
                self.record_name_change(
                    changed_by, new_username, old_username)

                from misago.users.signals import username_changed
                username_changed.send(sender=self)

    def record_name_change(self, changed_by, new_username, old_username):
        self.namechanges.create(new_username=new_username,
                                old_username=old_username,
                                changed_by=changed_by,
                                changed_by_username=changed_by.username)

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

    def is_following(self, user):
        try:
            self.follows.get(id=user.pk)
            return True
        except User.DoesNotExist:
            return False

    def is_blocking(self, user):
        try:
            self.blocks.get(id=user.pk)
            return True
        except User.DoesNotExist:
            return False


class Online(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True,
                                related_name='online_tracker')
    current_ip = models.GenericIPAddressField()
    last_click = models.DateTimeField(default=timezone.now)
    is_visible_on_index = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            super(Online, self).save(*args, **kwargs)
        except IntegrityError:
            pass # first come is first serve in online tracker


class UsernameChange(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='namechanges')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True, blank=True,
                                   related_name='user_renames',
                                   on_delete=models.SET_NULL)
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
