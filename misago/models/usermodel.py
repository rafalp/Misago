import hashlib
from datetime import timedelta
import math
from random import choice
from path import path
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from django.core.cache import cache, InvalidCacheBackendError
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import RequestContext
from django.utils import timezone as tz_util
from django.utils.translation import ugettext_lazy as _
from misago.acl.builder import acl
from misago.conf import settings
from misago.monitor import monitor, UpdatingMonitor
from misago.signals import delete_user_content, rename_user, sync_user_profile
from misago.template.loader import render_to_string
from misago.utils.avatars import avatar_size
from misago.utils.strings import random_string, slugify
from misago.validators import validate_username, validate_password, validate_email

class UserManager(models.Manager):
    """
    User Manager provides us with some additional methods for users
    """
    def get_blank_user(self):
        blank_user = User(
                        join_date=tz_util.now(),
                        join_ip='127.0.0.1'
                        )
        return blank_user

    def resync_monitor(self):
        with UpdatingMonitor() as cm:
            monitor['users'] = self.filter(activation=0).count()
            monitor['users_inactive'] = self.filter(activation__gt=0).count()
            last_user = self.filter(activation=0).latest('id')
            monitor['last_user'] = last_user.pk
            monitor['last_user_name'] = last_user.username
            monitor['last_user_slug'] = last_user.username_slug

    def create_user(self, username, email, password, timezone=False, ip='127.0.0.1', agent='', no_roles=False, activation=0, request=False):
        token = ''
        if activation > 0:
            token = random_string(12)

        timezone = timezone or settings.default_timezone

        # Get first rank
        try:
            from misago.models import Rank
            default_rank = Rank.objects.filter(special=0).order_by('-order')[0]
        except IndexError:
            default_rank = None

        # Store user in database
        new_user = User(
                        last_sync=tz_util.now(),
                        join_date=tz_util.now(),
                        join_ip=ip,
                        join_agent=agent,
                        activation=activation,
                        token=token,
                        timezone=timezone,
                        rank=default_rank,
                        subscribe_start=settings.subscribe_start,
                        subscribe_reply=settings.subscribe_reply,
                        )

        validate_username(username)
        validate_password(password)
        new_user.set_username(username)
        new_user.set_email(email)
        new_user.set_password(password)
        new_user.full_clean()
        new_user.default_avatar()
        new_user.save(force_insert=True)

        # Set user roles?
        if not no_roles:
            from misago.models import Role
            new_user.roles.add(Role.objects.get(_special='registered'))
            new_user.make_acl_key()
            new_user.save(force_update=True)

        # Update forum stats
        with UpdatingMonitor() as cm:
            if activation == 0:
                monitor.increase('users')
                monitor['last_user'] = new_user.pk
                monitor['last_user_name'] = new_user.username
                monitor['last_user_slug'] = new_user.username_slug
            else:
                monitor.increase('users_inactive')

        # Return new user
        return new_user

    def get_by_email(self, email):
        return self.get(email_hash=hashlib.md5(email).hexdigest())

    def filter_stats(self, start, end):
        return self.filter(join_date__gte=start).filter(join_date__lte=end)

    def block_user(self, user):
        return User.objects.select_for_update().get(id=user.id)


class User(models.Model):
    """
    Misago User model
    """
    username = models.CharField(max_length=255)
    username_slug = models.SlugField(max_length=255, unique=True,
                                     error_messages={'unique': _("This user name is already in use by another user.")})
    email = models.EmailField(max_length=255, validators=[validate_email])
    email_hash = models.CharField(max_length=32, unique=True,
                                     error_messages={'unique': _("This email address is already in use by another user.")})
    password = models.CharField(max_length=255)
    password_date = models.DateTimeField()
    avatar_type = models.CharField(max_length=10, null=True, blank=True)
    avatar_image = models.CharField(max_length=255, null=True, blank=True)
    avatar_original = models.CharField(max_length=255, null=True, blank=True)
    avatar_temp = models.CharField(max_length=255, null=True, blank=True)
    _avatar_crop = models.CharField(max_length=255, null=True, blank=True, db_column='avatar_crop')
    signature = models.TextField(null=True, blank=True)
    signature_preparsed = models.TextField(null=True, blank=True)
    join_date = models.DateTimeField()
    join_ip = models.GenericIPAddressField()
    join_agent = models.TextField(null=True, blank=True)
    last_date = models.DateTimeField(null=True, blank=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    last_agent = models.TextField(null=True, blank=True)
    hide_activity = models.PositiveIntegerField(default=0)
    subscribe_start = models.PositiveIntegerField(default=0)
    subscribe_reply = models.PositiveIntegerField(default=0)
    receive_newsletters = models.BooleanField(default=True)
    threads = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    votes = models.PositiveIntegerField(default=0)
    karma_given_p = models.PositiveIntegerField(default=0)
    karma_given_n = models.PositiveIntegerField(default=0)
    karma_p = models.PositiveIntegerField(default=0)
    karma_n = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)
    ranking = models.PositiveIntegerField(default=0)
    rank = models.ForeignKey('Rank', null=True, blank=True, on_delete=models.SET_NULL)
    last_sync = models.DateTimeField(null=True, blank=True)
    follows = models.ManyToManyField('self', related_name='follows_set', symmetrical=False)
    ignores = models.ManyToManyField('self', related_name='ignores_set', symmetrical=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    last_post = models.DateTimeField(null=True, blank=True)
    last_vote = models.DateTimeField(null=True, blank=True)
    last_search = models.DateTimeField(null=True, blank=True)
    alerts = models.PositiveIntegerField(default=0)
    alerts_date = models.DateTimeField(null=True, blank=True)
    allow_pds = models.PositiveIntegerField(default=0)
    unread_pds = models.PositiveIntegerField(default=0)
    sync_pds = models.BooleanField(default=False)
    activation = models.IntegerField(default=0)
    token = models.CharField(max_length=12, null=True, blank=True)
    avatar_ban = models.BooleanField(default=False)
    avatar_ban_reason_user = models.TextField(null=True, blank=True)
    avatar_ban_reason_admin = models.TextField(null=True, blank=True)
    signature_ban = models.BooleanField(default=False)
    signature_ban_reason_user = models.TextField(null=True, blank=True)
    signature_ban_reason_admin = models.TextField(null=True, blank=True)
    timezone = models.CharField(max_length=255, default='utc')
    roles = models.ManyToManyField('Role')
    is_team = models.BooleanField(default=False)
    acl_key = models.CharField(max_length=12, null=True, blank=True)
    warning_level = models.PositiveIntegerField(default=0)
    warning_level_update_on = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    ACTIVATION_NONE = 0
    ACTIVATION_USER = 1
    ACTIVATION_ADMIN = 2
    ACTIVATION_CREDENTIALS = 3

    statistics_name = _('Users Registrations')

    class Meta:
        app_label = 'misago'

    def is_god(self):
        try:
            return self.is_god_cache
        except AttributeError:
            for user in settings.ADMINS:
                if user[1].lower() == self.email:
                    self.is_god_cache = True
                    return True
            self.is_god_cache = False
            return False

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_crawler(self):
        return False

    def is_protected(self):
        for role in self.roles.all():
            if role.protected:
                return True
        return False

    def lock_avatar(self):
        # Kill existing avatar and lock our ability to change it
        self.delete_avatar()
        self.avatar_ban = True

        # Pick new one from _locked gallery
        galleries = path(settings.STATICFILES_DIRS[0]).joinpath('avatars').joinpath('_locked')
        avatars_list = galleries.files('*.gif')
        avatars_list += galleries.files('*.jpg')
        avatars_list += galleries.files('*.jpeg')
        avatars_list += galleries.files('*.png')
        self.avatar_type = 'gallery'
        self.avatar_image = '/'.join(path(choice(avatars_list)).splitall()[-2:])

    def default_avatar(self):
        if settings.default_avatar == 'gallery':
            try:
                avatars_list = []
                try:
                    # First try, _default path
                    galleries = path(settings.STATICFILES_DIRS[0]).joinpath('avatars').joinpath('_default')
                    avatars_list += galleries.files('*.gif')
                    avatars_list += galleries.files('*.jpg')
                    avatars_list += galleries.files('*.jpeg')
                    avatars_list += galleries.files('*.png')
                except Exception as e:
                    pass
                # Second try, all paths
                if not avatars_list:
                    avatars_list = []
                    for directory in path(settings.STATICFILES_DIRS[0]).joinpath('avatars').dirs():
                        if not directory[-7:] == '_locked' and not directory[-7:] == '_thumbs':
                            avatars_list += directory.files('*.gif')
                            avatars_list += directory.files('*.jpg')
                            avatars_list += directory.files('*.jpeg')
                            avatars_list += directory.files('*.png')
                if avatars_list:
                    # Pick random avatar from list
                    self.avatar_type = 'gallery'
                    self.avatar_image = '/'.join(path(choice(avatars_list)).splitall()[-2:])
                    return True
            except Exception as e:
                pass

        self.avatar_type = 'gravatar'
        self.avatar_image = None
        return True

    def delete_avatar_temp(self):
        if self.avatar_temp:
            try:
                av_file = path(settings.MEDIA_ROOT + 'avatars/' + self.avatar_temp)
                if not av_file.isdir():
                    av_file.remove()
            except Exception:
                pass

        self.avatar_temp = None

    def delete_avatar_original(self):
        if self.avatar_original:
            try:
                av_file = path(settings.MEDIA_ROOT + 'avatars/' + self.avatar_original)
                if not av_file.isdir():
                    av_file.remove()
            except Exception:
                pass

        self.avatar_original = None

    def delete_avatar_image(self):
        if self.avatar_image:
            for size in settings.AVATAR_SIZES[1:]:
                try:
                    av_file = path(settings.MEDIA_ROOT + 'avatars/' + str(size) + '_' + self.avatar_image)
                    if not av_file.isdir():
                        av_file.remove()
                except Exception:
                    pass
            try:
                av_file = path(settings.MEDIA_ROOT + 'avatars/' + self.avatar_image)
                if not av_file.isdir():
                    av_file.remove()
            except Exception:
                pass

        self.avatar_image = None

    def delete_avatar(self):
        self.delete_avatar_temp()
        self.delete_avatar_original()
        self.delete_avatar_image()

    def delete_content(self):
        delete_user_content.send(sender=self)

    def delete(self, *args, **kwargs):
        self.delete_avatar()
        super(User, self).delete(*args, **kwargs)

    def set_username(self, username):
        self.username = username.strip()
        self.username_slug = slugify(username)

    def sync_username(self):
        rename_user.send(sender=self)

    def is_username_valid(self, e):
        try:
            raise ValidationError(e.message_dict['username'])
        except KeyError:
            pass
        try:
            raise ValidationError(e.message_dict['username_slug'])
        except KeyError:
            pass

    def is_email_valid(self, e):
        try:
            raise ValidationError(e.message_dict['email'])
        except KeyError:
            pass
        try:
            raise ValidationError(e.message_dict['email_hash'])
        except KeyError:
            pass

    def is_password_valid(self, e):
        try:
            raise ValidationError(e.message_dict['password'])
        except KeyError:
            pass

    def set_email(self, email):
        self.email = email.strip().lower()
        self.email_hash = hashlib.md5(self.email).hexdigest()

    def set_password(self, raw_password):
        self.password_date = tz_util.now()
        self.password = make_password(raw_password.strip())

    def set_last_visit(self, ip, agent):
        self.last_date = tz_util.now()
        self.last_ip = ip
        self.last_agent = agent

    def check_password(self, raw_password, mobile=False):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()

        # Is standard password allright?
        if check_password(raw_password, self.password, setter):
            return True

        # Check mobile password?
        if mobile:
            raw_password = raw_password[:1].lower() + raw_password[1:]
        else:
            password_reversed = u''
            for c in raw_password:
                r = c.upper()
                if r == c:
                    r = c.lower()
                password_reversed += r
            raw_password = password_reversed
        return check_password(raw_password, self.password, setter)

    def is_following(self, user):
        try:
            return self.follows.filter(id=user.pk).count() > 0
        except AttributeError:
            return self.follows.filter(id=user).count() > 0

    def is_ignoring(self, user):
        try:
            return self.ignores.filter(id=user.pk).count() > 0
        except AttributeError:
            return self.ignores.filter(id=user).count() > 0

    def ignored_users(self):
        return [item['id'] for item in self.ignores.values('id')]

    def allow_pd_invite(self, user):
        # PD's from nobody
        if self.allow_pds == 3:
            return False
        # PD's from followed
        if self.allow_pds == 2:
            return self.is_following(user)
        # PD's from non-ignored
        if self.allow_pds == 1:
            return not self.is_ignoring(user)
        return True

    def get_roles(self):
        if self.rank:
            return self.roles.all() | self.rank.roles.all()
        return self.roles.all()

    def make_acl_key(self, force=False):
        if not force and self.acl_key:
            return self.acl_key
        roles_ids = []
        for role in self.roles.all():
            roles_ids.append(role.pk)
        if self.rank:
            for role in self.rank.roles.all():
                if not role.pk in roles_ids:
                    roles_ids.append(role.pk)
        roles_ids.sort()
        self.acl_key = 'acl_%s' % hashlib.md5('_'.join(str(x) for x in roles_ids)).hexdigest()[0:8]
        self.save(update_fields=('acl_key',))
        return self.acl_key

    def acl(self):
        return acl(self)

    @property
    def avatar_crop(self):
        return [int(float(x)) for x in self._avatar_crop.split(',')] if self._avatar_crop else (0, 0, 100, 100)

    @avatar_crop.setter
    def avatar_crop(self, value):
        self._avatar_crop = ','.join(value)

    def get_avatar(self, size=None):
        image_size = avatar_size(size) if size else None

        # Get uploaded avatar
        if self.avatar_type == 'upload':
            image_prefix = '%s_' % image_size if image_size else ''
            return settings.MEDIA_URL + 'avatars/' + image_prefix + self.avatar_image

        # Get gallery avatar
        if self.avatar_type == 'gallery':
            image_prefix = '_thumbs/%s/' % image_size if image_size else ''
            return settings.STATIC_URL + 'avatars/' + image_prefix + self.avatar_image

        # No avatar found, get gravatar
        if not image_size:
            image_size = settings.AVATAR_SIZES[0]

        # Decide on default gravatar
        gravatar_default = ''
        if (settings.GRAVATAR_DEFAULT
                and not '&' in settings.GRAVATAR_DEFAULT
                and not '?' in settings.GRAVATAR_DEFAULT):
            gravatar_default = '&d=%s' % settings.GRAVATAR_DEFAULT

        return 'http://www.gravatar.com/avatar/%s?s=%s%s' % (hashlib.md5(self.email).hexdigest(), image_size, gravatar_default)

    def get_ranking(self):
        if not self.ranking:
            self.ranking = User.objects.filter(score__gt=self.score).count() + 1
            self.save(force_update=True)
        return self.ranking

    def get_title(self):
        if self.title:
            return self.title
        if self.rank:
            return self.rank.title
        return None

    def get_style(self):
        if self.rank:
            return self.rank.style
        return ''

    def email_user(self, request, template, subject, context={}):
        context = RequestContext(request, context)
        context['author'] = context['user']
        context['user'] = self

        email_html = render_to_string('_email/%s.html' % template,
                                      context_instance=context)
        email_text = render_to_string('_email/%s.txt' % template,
                                      context_instance=context)

        # Set message recipient
        if settings.DEBUG and settings.CATCH_ALL_EMAIL_ADDRESS:
            recipient = settings.CATCH_ALL_EMAIL_ADDRESS
        else:
            recipient = self.email

        # Set message author
        if settings.board_name:
            sender = '%s <%s>' % (settings.board_name.replace("<", "(").replace(">", ")"), settings.EMAIL_HOST_USER)
        else:
            sender = settings.EMAIL_HOST_USER

        # Build message and add it to queue
        email = EmailMultiAlternatives(subject, email_text, sender, [recipient])
        email.attach_alternative(email_html, "text/html")
        request.mails_queue.append(email)

    def get_activation(self):
        activations = ['none', 'user', 'admin', 'credentials']
        return activations[self.activation]

    def alert(self, message):
        from misago.models import Alert
        self.alerts += 1
        return Alert(user=self, message=message, date=tz_util.now())

    def sync_unread_pds(self, unread):
        self.unread_pds = unread
        self.sync_pds = False

    def get_date(self):
        return self.join_date

    def sync_profile(self):
        if (settings.PROFILES_SYNC_FREQUENCY > 0 and
                self.last_sync <= tz_util.now() - timedelta(days=settings.PROFILES_SYNC_FREQUENCY)):
            sync_user_profile.send(sender=self)
            self.last_sync = tz_util.now()
            return True
        return False

    def is_warning_level_expired(self):
        if self.warning_level and self.warning_level_update_on:
            return tz_util.now() > self.warning_level_update_on
        return False

    def update_expired_warning_level(self):
        self.warning_level -= 1

        try:
            from misago.models import WarnLevel
            warning_levels = WarnLevel.objects.get_levels()
            new_warning_level = warning_levels[self.warning_level]
            if new_warning_level.expires_after_minutes:
                self.warning_level_update_on -= timedelta(
                    minutes=new_warning_level.expires_after_minutes)
            else:
                self.warning_level_update_on = None
        except KeyError:
            # Break expiration chain so infinite loop won't happen
            # This should only happen if your warning level is 0, but
            # will also keep app responsive if data corruption happens
            self.warning_level_update_on = None

    def get_warning_level(self):
        if self.warning_level:
            from misago.models import WarnLevel
            return WarnLevel.objects.get_level(
                self.warning_level)
        else:
            return None

    def get_current_warning_level(self):
        if self.is_warning_level_expired():
            while self.update_expired_warning_level():
                self.update_warning_level()
            self.save(force_update=True)

        return self.get_warning_level()

    def timeline(self, qs, length=100):
        posts = {}
        now = tz_util.now()
        for item in qs.iterator():
            diff = (now - item.timeline_date).days
            try:
                posts[diff] += 1
            except KeyError:
                posts[diff] = 1

        graph = []
        for i in reversed(range(100)):
            try:
                graph.append(posts[i])
            except KeyError:
                graph.append(0)
        return graph


class Guest(object):
    """
    Misago Guest dummy
    """
    id = -1
    pk = -1
    is_team = False

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return False

    def is_crawler(self):
        return False

    def get_roles(self):
        from misago.models import Role
        return Role.objects.filter(_special='guest')

    def make_acl_key(self):
        return 'acl_guest'


class Crawler(Guest):
    """
    Misago Crawler dummy
    """
    is_team = False

    def __init__(self, username):
        self.username = username

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return False

    def is_crawler(self):
        return True


"""
Signals handlers
"""
def sync_user_handler(sender, **kwargs):
    sender.following = sender.follows.count()
    sender.followers = sender.follows_set.count()

sync_user_profile.connect(sync_user_handler, dispatch_uid="sync_user_follows")