from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager as BaseUserManager,
                                        AnonymousUser as DjangoAnonymousUser)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.acl import get_user_acl
from misago.acl.models import Role
from misago.admin import site
from misago.core.utils import slugify
from misago.users.models import Rank
from misago.users.utils import hash_email
from misago.users.validators import (validate_email, validate_password,
                                     validate_username)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
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
            user.rank = Rank.objects.default()

        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password=password)
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
    rank = models.ForeignKey(
        'users.Rank', null=True, blank=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False, db_index=True,
        help_text=_('Designates whether the user can log into admin sites.'))
    roles = models.ManyToManyField('acl.Role')
    acl_key = models.CharField(max_length=12, null=True, blank=True)

    is_active = True

    USERNAME_FIELD = 'username_slug'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        app_label = 'users'

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

        return [roles_dict[r] for r in roles_pks]

    def update_acl_key(self):
        pass


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


"""register model in misago admin"""
site.add_node(
    parent='misago:admin',
    after='misago:admin:index',
    namespace='misago:admin:users',
    link='misago:admin:users:accounts:index',
    name=_("Users"),
    icon='fa fa-users')

site.add_node(
    parent='misago:admin:users',
    namespace='misago:admin:users:accounts',
    link='misago:admin:users:accounts:index',
    name=_("User Accounts"),
    icon='fa fa-users')
