from django.core.exceptions import ValidationError
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager as BaseUserManager)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.core.utils import slugify
from misago.users.utils import hash_email
from misago.users.validators import (validate_email, validate_password,
                                     validate_username)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("User must have an email address."))

        try:
            validate_username(username)
            validate_email(email)
            validate_password(password)
        except ValidationError as e:
            raise ValueError(unicode(e))

        now = timezone.now()
        user = self.model(is_staff=False, is_superuser=False, last_login=now,
                          joined_on=now, **extra_fields)

        user.set_username(username)
        user.set_email(email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
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
    is_staff = models.BooleanField(
        _('staff status'), default=False, db_index=True,
        help_text=_('Designates whether the user can log into admin sites.'))
    is_active = True

    USERNAME_FIELD = 'username_slug'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        app_label = 'users'

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
