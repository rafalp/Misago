from datetime import timedelta
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.db.models.loading import cache as model_cache
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.utils.encoding import force_unicode
from misago.authn.methods import auth_remember, AuthException
from misago.sessions.models import *
from misago.users.models import Guest, User
from misago.utils import get_random_string

# Assert models are loaded
if not model_cache.loaded:
    model_cache.get_models()
    
    
class IncorrectSessionException(Exception):
    pass

    
class SessionMisago(SessionBase):
    """
    Abstract class for sessions to inherit and extend
    """
    def _get_new_session_key(self):
        return get_random_string(42)
      
    def _get_session(self):
        try:
            return self._session_cache
        except AttributeError:
            self._session_cache = self.load()
        return self._session_cache
        
    def _hash(self, value):
        key_salt = "misago.sessions" + self.__class__.__name__
        return salted_hmac(key_salt, value).hexdigest()
       
    def delete(self):
        """We use sessions to track onlines so sorry, only sessions cleaner may delete sessions"""
        pass
       
    def flush(self):
        """We use sessions to track onlines so sorry, only sessions cleaner may delete sessions"""
        pass

    def load(self):
        return self.decode(force_unicode(self._session_rk.data))
    
    def session_expired(self):
        return False
        
    def get_hidden(self):
        return False
    
    def set_hidden(self, hidden=False):
        pass
    
    def get_ip(self, request):
        return request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')
    
    def set_user(self, user = None):
        pass
    
    def get_ban(self):
        return False
    
    def set_ban(self, ban):
        return False
    
    def save(self, request, response):
        self._session_rk.data = self.encode(self._get_session())
        self._session_rk.last = timezone.now()
        self._session_rk.save(force_update=True)


class SessionCrawler(SessionMisago):
    """
    Crawler Session controller
    """
    def __init__(self, request):
        self._ip = self.get_ip(request)
        try:
            self._session_rk = Session.objects.get(crawler=request.user.username, ip=self._ip)
            self._session_key = self._session_rk.id
        except Session.DoesNotExist:
            self.create(request)
            
    def create(self, request):
        while True:
            try:
                self._session_key = self._get_new_session_key()
                self._session_rk = Session(
                                         id=self._session_key,
                                         data=self.encode({}),
                                         crawler=request.user.username,
                                         ip=self._ip,
                                         agent=request.META.get('HTTP_USER_AGENT', ''),
                                         start=timezone.now(),
                                         last=timezone.now(),
                                         matched=True
                                         )
                self._session_rk.save(force_insert=True)
                break
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            
    def human_session(self):
        return False


class SessionHuman(SessionMisago):
    """
    Human Session controller
    """
    def __init__(self, request):
        self.expired = False
        self.hidden = False
        self.team = False
        self.remember_me = None
        self._user = None
        self._ip = self.get_ip(request)
        self._session_token = None
        if request.firewall.admin:
            self._cookie_sid = settings.COOKIES_PREFIX + 'ASID'
        else:   
            self._cookie_sid = settings.COOKIES_PREFIX + 'SID'
        try:
            # Do we have correct session ID?
            if self._cookie_sid not in request.COOKIES or len(request.COOKIES[self._cookie_sid]) != 42:
                raise IncorrectSessionException()
            self._session_key = request.COOKIES[self._cookie_sid]
            self._session_rk = Session.objects.select_related().get(
                                                                    pk=self._session_key,
                                                                    admin=request.firewall.admin
                                                                    )
            # IP invalid
            if request.settings.sessions_validate_ip and self._session_rk.ip != self._ip:
                raise IncorrectSessionException()
            # Session expired
            if timezone.now() - self._session_rk.last > timedelta(seconds=settings.SESSION_LIFETIME):
                self.expired = True
                raise IncorrectSessionException()
            # Change session to matched and extract session user and hidden flag
            self._session_rk.matched = True
            self._user = self._session_rk.user
            self.hidden = self._session_rk.hidden
        except (Session.DoesNotExist, IncorrectSessionException):
            # Attempt autolog
            try:
                self.remember_me = auth_remember(request, self.get_ip(request))
                self.create(request, user=self.remember_me.user, hidden=self.remember_me.hidden)
            except AuthException as e:
                # Autolog failed
                self.create(request)
        self.id = self._session_rk.id        
        
        # Make cookie live longer
        if request.firewall.admin:
            request.cookie_jar.set('ASID', self._session_rk.id)
        else:   
            request.cookie_jar.set('SID', self._session_rk.id)
            
    def create(self, request, user=None):
        self._user = user
        while True:
            try:
                self._session_key = self._get_new_session_key()
                self._session_rk = Session(
                                         id=self._session_key,
                                         data=self.encode({}),
                                         user=self._user,
                                         ip=self._ip,
                                         agent=request.META.get('HTTP_USER_AGENT', ''),
                                         start=timezone.now(),
                                         last=timezone.now(),
                                         admin=request.firewall.admin,
                                         )
                self._session_rk.save(force_insert=True)
                if user:
                    # Update user data
                    user.set_last_visit(
                                        self.get_ip(request),
                                        request.META.get('HTTP_USER_AGENT', ''),
                                        hidden=self.hidden
                                        )
                    user.save(force_update=True)
                break
            except CreateError:
                # Key wasn't unique. Try again.
                continue
    
    def save(self, request, response):
        self._session_rk.user = self._user
        self._session_rk.hidden = self.hidden
        self._session_rk.team = self.team
        super(SessionHuman, self).save(request, response)
        
    def human_session(self):
        return True
    
    def session_expired(self):
        return self.expired
        
    def get_user(self):
        if self._user == None:
            return Guest()
        return self._user
    
    def set_user(self, user=None):
        self._user = user
    
    def sign_out(self, request):
        try:
            if self._user.is_authenticated():
                if not request.firewall.admin:
                    cookie_token = settings.COOKIES_PREFIX + 'TOKEN'
                    if cookie_token in request.COOKIES:
                        if len(request.COOKIES[cookie_token]) > 0:
                            Token.objects.filter(id=request.COOKIES[cookie_token]).delete()
                        request.cookie_jar.delete('TOKEN')
                self.hidden = False
                self._user = None
                request.user = Guest()
        except AttributeError:
            pass
        
    def get_hidden(self):
        return self.hidden
    
    def set_hidden(self, hidden=False):
        self.hidden = hidden