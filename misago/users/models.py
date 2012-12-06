import hashlib
import math
from random import choice
from path import path
from django.conf import settings
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import RequestContext
from django.utils import timezone as tz_util
from django.utils.translation import ugettext_lazy as _
from misago.monitor.monitor import Monitor
from misago.settings.settings import Settings as DBSettings
from misago.users.validators import validate_username, validate_password, validate_email
from misago.utils import get_random_string, slugify

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
    
    def resync_monitor(self, monitor):
        monitor['users'] = self.count()
        monitor['users_inactive'] = self.filter(activation__gt=0).count()
        last_user = self.latest('id')
        monitor['last_user'] = last_user.pk
        monitor['last_user_name'] = last_user.username
        monitor['last_user_slug'] = last_user.username_slug
    
    def create_user(self, username, email, password, timezone=False, ip='127.0.0.1', no_roles=False, activation=0, request=False):
        token = ''
        if activation > 0:
            token = get_random_string(12)
        
        try:
            db_settings = request.settings
        except AttributeError:
            db_settings = DBSettings()
            
        if timezone == False:
            timezone = db_settings['default_timezone']
        
        # Get first rank
        try:
            from misago.ranks.models import Rank
            default_rank = Rank.objects.filter(special=0).order_by('order')[0]
        except Rank.DoesNotExist:
            default_rank = None
        
        # Store user in database
        new_user = User(
                        last_sync=tz_util.now(),
                        join_date=tz_util.now(),
                        join_ip=ip,
                        activation=activation,
                        token=token,
                        timezone=timezone,
                        rank=default_rank,
                        )
        
        new_user.set_username(username)
        new_user.set_email(email)
        new_user.set_password(password)
        new_user.full_clean()
        new_user.default_avatar(db_settings)
        new_user.save(force_insert=True)
        
        # Set user roles?
        if not no_roles:
            from misago.roles.models import Role
            new_user.roles.add(Role.objects.get(token='registered'))
            new_user.save(force_update=True)
        
        # Load monitor
        try:
            monitor = request.monitor
        except AttributeError:
            monitor = Monitor()
        
        # Update forum stats
        if activation == 0:
            monitor['users'] = int(monitor['users']) + 1
            monitor['last_user'] = new_user.pk
            monitor['last_user_name'] = new_user.username
            monitor['last_user_slug'] = new_user.username_slug
        else:
            monitor['users_inactive'] = int(monitor['users_inactive']) + 1
            
        # Return new user
        return new_user
            
    def get_by_email(self, email):
        return self.get(email_hash=hashlib.md5(email).hexdigest())
    
    def filter_stats(self, start, end):
        return self.filter(join_date__gte=start).filter(join_date__lte=end)
    
        
class User(models.Model):
    """
    Misago User model
    """
    username = models.CharField(max_length=255,validators=[validate_username])
    username_slug = models.SlugField(max_length=255,unique=True,
                                     error_messages={'unique': _("This user name is already in use by another user.")})
    email = models.EmailField(max_length=255,validators=[validate_email])
    email_hash = models.CharField(max_length=32,unique=True,
                                     error_messages={'unique': _("This email address is already in use by another user.")})
    password = models.CharField(max_length=255)
    password_date = models.DateTimeField()
    avatar_type = models.CharField(max_length=10,null=True,blank=True)
    avatar_image = models.CharField(max_length=255,null=True,blank=True)
    signature = models.TextField(null=True,blank=True)
    signature_preparsed = models.TextField(null=True,blank=True)
    join_date = models.DateTimeField()
    join_ip = models.GenericIPAddressField()
    join_agent = models.TextField(null=True,blank=True)
    last_date = models.DateTimeField(null=True,blank=True)
    last_ip = models.GenericIPAddressField(null=True,blank=True)
    last_agent = models.TextField(null=True,blank=True)
    hide_activity = models.PositiveIntegerField(default=0)
    alert_ats = models.PositiveIntegerField(default=0)
    allow_pms = models.PositiveIntegerField(default=0)
    receive_newsletters = models.BooleanField(default=True)
    topics = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    votes = models.PositiveIntegerField(default=0)
    karma_given_p = models.PositiveIntegerField(default=0)
    karma_given_n = models.PositiveIntegerField(default=0)
    karma_p = models.PositiveIntegerField(default=0)
    karma_n = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0,db_index=True)
    rank = models.ForeignKey('ranks.Rank',null=True,blank=True,db_index=True,on_delete=models.SET_NULL)
    last_sync = models.DateTimeField(null=True,blank=True)
    follows = models.ManyToManyField('self',related_name='follows_set',symmetrical=False)
    ignores = models.ManyToManyField('self',related_name='ignores_set',symmetrical=False)
    title = models.CharField(max_length=255,null=True,blank=True)
    last_post = models.DateTimeField(null=True,blank=True)
    last_search = models.DateTimeField(null=True,blank=True)
    alerts = models.PositiveIntegerField(default=0)
    alerts_new = models.PositiveIntegerField(default=0)
    activation = models.IntegerField(default=0)
    token = models.CharField(max_length=12,null=True,blank=True)
    avatar_ban = models.BooleanField(default=False)
    avatar_ban_reason_user = models.TextField(null=True,blank=True)
    avatar_ban_reason_admin = models.TextField(null=True,blank=True)
    signature_ban = models.BooleanField(default=False)
    signature_ban_reason_user = models.TextField(null=True,blank=True)
    signature_ban_reason_admin = models.TextField(null=True,blank=True)
    timezone = models.CharField(max_length=255,default='utc')
    roles = models.ManyToManyField('roles.Role')
    acl_cache = models.TextField(null=True,blank=True)
    
    objects = UserManager()   
    
    ACTIVATION_NONE = 0
    ACTIVATION_USER = 1
    ACTIVATION_ADMIN = 2
    ACTIVATION_CREDENTIALS = 3
    
    statistics_name = _('Users Registrations')
        
    def acl(self):
        pass
        
    def is_admin(self):
        if self.is_god():
            return True
        return False #TODO!
    
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
        
    def default_avatar(self, db_settings):
        if db_settings['default_avatar'] == 'gallery':
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
                        if not directory[-7:] == '_locked':
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

    def delete_avatar(self):
        if self.avatar_type == 'upload':
            # DELETE OUR AVATAR!!!
            pass
    
    def delete_content(self):
        if self.pk:
            for model_obj in models.get_models():
                try:
                    model_obj.objects.delete_user_content(self)
                except AttributeError:
                    pass
    
    def delete(self, *args, **kwargs):
        self.delete_avatar()
        super(User, self).delete(*args, **kwargs)
            
    def set_username(self, username):
        self.username = username.strip()
        self.username_slug = slugify(username)
        
        if self.pk:
            for model_obj in models.get_models():
                try:
                    model_obj.objects.update_username(self)
                except AttributeError:
                    pass
     
    def set_signature(self, signature):
        self.signature = signature.strip()
        self.signature_preparsed = ''
        if self.signature:
            import markdown
            self.signature_preparsed = markdown.markdown(value, safe_mode='escape', output_format=settings.OUTPUT_FORMAT)
        
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

    def set_last_visit(self, ip, agent, hidden=False):
        self.last_date = tz_util.now()
        self.last_ip = ip
        self.last_agent = agent
        self.last_hide = hidden

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
    
    def get_avatar(self, size='normal'):
        # Get uploaded avatar
        if self.avatar_type == 'upload':
            return settings.MEDIA_URL + 'avatars/' + self.avatar_image
        
        # Get gallery avatar
        if self.avatar_type == 'gallery':
            return settings.STATIC_URL + 'avatars/' + self.avatar_image
        
        # No avatar found, get gravatar
        if size == 'big':
            size = 150;
        elif size == 'small':
            size = 64;
        elif size == 'tiny':
            size = 46;
        else:
            size = 100
        return 'http://www.gravatar.com/avatar/%s?s=%s' % (hashlib.md5(self.email).hexdigest(), size)
    
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
        templates = request.theme.get_email_templates(template)
        context = RequestContext(request, context)
        context['author'] = context['user']
        context['user'] = self
        
        # Set message recipient
        if settings.DEBUG and settings.CATCH_ALL_EMAIL_ADDRESS:
            recipient = settings.CATCH_ALL_EMAIL_ADDRESS
        else:
            recipient = self.email
            
        # Build and send message
        email = EmailMultiAlternatives(subject, templates[0].render(context), settings.EMAIL_HOST_USER, [recipient])
        email.attach_alternative(templates[1].render(context), "text/html")
        email.send()
    
    def get_activation(self):
        activations = ['none', 'user', 'admin', 'credentials']
        return activations[self.activation]
    
    def get_date(self):
        return self.join_date
    
    def sync_user(self):
        print 'SYNCING USER!'    
        
class Guest(object):
    """
    Misago Guest dummy
    """
    def is_admin(self):
        return False
    
    def is_anonymous(self):
        return True
    
    def is_authenticated(self):
        return False
    
    def is_crawler(self):
        return False
        
        
class Crawler(object): 
    """
    Misago Crawler dummy
    """
    def __init__(self, username):
        self.username = username
    
    def is_admin(self):
        return False
    
    def is_anonymous(self):
        return True
    
    def is_authenticated(self):
        return False
    
    def is_crawler(self):
        return True

