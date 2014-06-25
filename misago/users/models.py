from hashlib import md5
import re
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager as BaseUserManager,
                                        AnonymousUser as DjangoAnonymousUser)
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.acl import get_user_acl, version as acl_version
from misago.acl.models import Role
from misago.core.utils import slugify
from misago.users.utils import hash_email
from misago.users.validators import (validate_email, validate_password,
                                     validate_username)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        with transaction.atomic():
            if not email:
                raise ValueError(_("User must have an email address."))
            if not password:
                raise ValueError(_("User must have a password."))

            validate_username(username)
            validate_email(email)
            validate_password(password)

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
    last_active = models.DateTimeField(null=True, blank=True)
    rank = models.ForeignKey(
        'Rank', null=True, blank=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, null=True, blank=True)
    activation_requirement = models.PositiveIntegerField(default=0)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into admin sites.'))
    roles = models.ManyToManyField('misago_acl.Role')
    acl_key = models.CharField(max_length=12, null=True, blank=True)

    is_active = True

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
            roles_dict[role.pk] = role

        if self.rank:
            for role in self.rank.roles.all():
                if role.pk not in roles_pks:
                    roles_pks.append(role.pk)
                    roles_dict[role.pk] = role

        return [roles_dict[r] for r in sorted(roles_pks)]

    def update_acl_key(self):
        roles_pks = [unicode(r.pk) for r in self.get_roles()]
        self.acl_key = md5(','.join(roles_pks)).hexdigest()[:12]


class Online(models.Model):
    user = models.OneToOneField(User, primary_key=True,
                                related_name='online_tracker')
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


"""
Ranks
"""
class RankManager(models.Manager):
    def get_default(self):
        return self.get(is_default=True)

    def make_rank_default(self, rank):
        with transaction.atomic():
            self.filter(is_default=True).update(is_default=False)
            rank.is_default = True
            rank.save(update_fields=['is_default'])


class Rank(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    roles = models.ManyToManyField('misago_acl.Role', null=True, blank=True)
    css_class = models.CharField(max_length=255, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    is_tab = models.BooleanField(default=False)
    is_on_index = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    objects = RankManager()

    class Meta:
        get_latest_by = 'order'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_order()
        else:
            acl_version.invalidate()
        return super(Rank, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        acl_version.invalidate()
        return super(Rank, self).delete(*args, **kwargs)

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)

    def set_order(self):
        try:
            self.order = Rank.objects.latest('order').order + 1
        except Rank.DoesNotExist:
            self.order = 0


"""
Bans
"""
BAN_NAME = 0
BAN_EMAIL = 1
BAN_IP = 2


class BansManager(models.Manager):
    def is_ip_banned(self, ip):
        return self.check_ban(ip=ip)

    def is_username_banned(self, username):
        return self.check_ban(username=username)

    def is_email_banned(self, email):
        return self.check_ban(email=email)

    def check_ban(self, username=None, email=None, ip=None):
        tests = []

        if username:
            tests.append(BAN_NAME)
        if email:
            tests.append(BAN_EMAIL)
        if ip:
            tests.append(BAN_IP)

        queryset = self.filter(is_valid=False)
        if len(tests) == 1:
            queryset = queryset.filter(test=tests[0])
        elif tests:
            queryset = queryset.filter(test__in=tests)

        for ban in queryset.order_by('-id').iterator():
            if username and ban.test == BAN_NAME and ban.test_value(username):
                return ban
            elif email and ban.test == BAN_EMAIL and ban.test_value(email):
                return ban
            elif ip and ban.test == BAN_IP and ban.test_value(ip):
                return ban
        return False


class Ban(models.Model):
    test = models.PositiveIntegerField(default=BAN_NAME, db_index=True)
    banned_value = models.CharField(max_length=255, db_index=True)
    reason_user = models.TextField(null=True, blank=True)
    reason_admin = models.TextField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True, db_index=True)
    is_valid = models.BooleanField(default=False, db_index=True)

    objects = BansManager()

    def test_value(self, value):
        regex = '^' + re.escape(self.banned_value).replace('\*', '(.*?)') + '$'
        return re.search(regex, value, flags=re.IGNORECASE)


class BanCache(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    bans_version = models.PositiveIntegerField(default=0)
    valid_until = models.DateField(null=True, blank=True)
