===============
Misago with CAS
===============

Making Misago work with `CAS <https://www.apereo.org/projects/cas>`_ (after it's been fully configured and it works) is a matter of:

1. Making a custom login class called `CASBackend2` which disables the default avatars, and prevents Misago from storing passwords and emails in Misago's User object. You could use LDAP to store these.

2. Modifying the template by adding a login url to /login

3. Installing django_cas_ng: `pip install django_cas_ng`

4. Modifying the `urls.py`.

============
The process:
============

Go in `urls.py` and add:

.. code-block:: python

  from django_cas_ng import views as django_cas_ng_views
  urlpatterns = [
      url(r'^forum/login$', django_cas_ng_views.login),
      url(r'^forum/logout$', django_cas_ng_views.logout),
	  # ... the rest

Go in settings.py and add:

.. code-block:: python

  AUTHENTICATION_BACKENDS = (
      'misago.users.authbackends.MisagoBackend',
      'plugins.CASBackend2.CASBackend2'
  )
  
  CAS_SERVER_URL = "http://192.168.35.30:8080/cas/"
  
  
  from django.utils.translation import ugettext_lazy as _
  CAS_ADMIN_PREFIX = None
  CAS_CREATE_USER = True
  CAS_EXTRA_LOGIN_PARAMS = None
  CAS_RENEW = False
  CAS_IGNORE_REFERER = False
  CAS_LOGOUT_COMPLETELY = True
  CAS_FORCE_CHANGE_USERNAME_CASE = "lower"
  CAS_REDIRECT_URL = '/forum/'
  CAS_RETRY_LOGIN = False
  CAS_VERSION = '2'
  CAS_USERNAME_ATTRIBUTE = 'uid'
  CAS_LOGIN_MSG = _("Login succeeded. Welcome, %s.")
  CAS_LOGGED_MSG = _("You are logged in as %s.")
  
  CAS_LOGOUT_COMPLETELY = True
  CAS_EXTRA_LOGIN_PARAMS = {'renew': True}

Create a folder "plugins" with a "__init__.py" file inside and also a file called `CASBackend2.py`. Copy paste the following inside:

.. code-block:: python

  """CAS authentication backend"""
  from __future__ import absolute_import
  from __future__ import unicode_literals
  
  from django.contrib.auth import authenticate, get_user_model, login
  from django.core.exceptions import PermissionDenied
  from django.utils.translation import ugettext as _
  from django.views.decorators.csrf import csrf_protect
  
  from misago.users.models import ACTIVATION_REQUIRED_ADMIN, ACTIVATION_REQUIRED_USER, ACTIVATION_REQUIRED_NONE
  
  from django.contrib.auth import get_user_model
  from django.contrib.auth.backends import ModelBackend
  from django.conf import settings
  
  from django_cas_ng.signals import cas_user_authenticated
  from django_cas_ng.utils import get_cas_client
  
  User = get_user_model()
  #from django.contrib.auth.models import User
  __all__ = ['CASBackend2']
  
  from django.utils.crypto import get_random_string
  
  import string
  class CASBackend2(ModelBackend):
      """CAS authentication backend"""
  
      def authenticate(self, ticket, service, request):
          global settings
          email = get_random_string(length=12) + "@email.email" #ignore email
  
          client = get_cas_client(service_url=service)
          username, attributes, pgtiou = client.verify_ticket(ticket)
  
          if attributes:
              request.session['attributes'] = attributes
          if not username:
              return None
  
          username_case = settings.CAS_FORCE_CHANGE_USERNAME_CASE
          if username_case == 'lower':
              username = username.lower()
          elif username_case == 'upper':
              username = username.upper()
  
          try:
              user = User.objects.get(**{User.USERNAME_FIELD: username})
              created = False
          except User.DoesNotExist:
              # check if we want to create new users, if we don't fail auth
              if not settings.CAS_CREATE_USER:
                  return None
              # user will have an "unusable" password
  
              user = User.objects.create_user(
                  username,
                  email,
                  password="PASS" + get_random_string(length=12) + "WORD", #ignore password
                  joined_from_ip="0.0.0.0",
                  set_default_avatar=False, # ignore avatar
                  requires_activation=ACTIVATION_REQUIRED_NONE #ignore activation
              )
              user.save()
              created = True
  
          if not self.user_can_authenticate(user):
              return None
  
          if pgtiou and settings.CAS_PROXY_CALLBACK:
              request.session['pgtiou'] = pgtiou
  
          # send the `cas_user_authenticated` signal
          cas_user_authenticated.send(
              sender=self,
              user=user,
              created=created,
              attributes=attributes,
              ticket=ticket,
              service=service,
          )
          return user
  
      def user_can_authenticate(self, user):
          return True
  
      def get_user(self, user_id):
          """Retrieve the user's entry in the User model if it exists"""
  
          try:
              return User.objects.get(pk=user_id)
          except User.DoesNotExist:
              return None


Now, go in 127.0.0.1/login and it should redirect to your CAS SERVER ip (the one configured in `settings.py`). Put your credentials in as you'd usually do, and you should be returned to Misago loggedin.