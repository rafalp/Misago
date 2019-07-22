=====================
Misago Single Sign ON
=====================

Client
======

In Misago instance set settings::

    SSO_PRIVATE_KEY = 'MySecretKey'
    SSO_PUBLIC_KEY = 'MyPublicKey'
    SSO_SERVER = "http://www.example.com/server/"

Server
======

Example django server instance config:

1. Install django-simple-sso: ``pip install django-simple-sso``
2. Run migrations: ``./manage.py migrate``
3. Create ``Consumer`` object in shell: ``./manage.py shell``::

    > from simple_sso.sso_server.models import Consumer
    > Consumer.objects.create(public_key='MyPublicKey',
    ... private_key='MySecretKey', name='MyAppName')

4. Add ``'simple_sso.sso_server'`` to ``INSTALLED_APPS``
5. Initialize server and add urls to ``urls.py``::

    from simple_sso.sso_server.server import Server
    my_server = Server()
    urlpatterns += [
        url(r'^server/', include(my_server.get_urls())),
    ]

How to test
===========

In your web browser Go to site ``http://localhost:8000/sso/client/``. You should be redirected to
login on your ``server`` site. After logging you will back to Misago and you will be logged as a
user from ``server`` site.

External docs
=============

Soruce code
-----------

* https://github.com/divio/django-simple-sso

Docs sites
----------

* https://micropyramid.com/blog/django-single-sign-on-sso-to-multiple-applications/
* https://medium.com/@MicroPyramid/django-single-sign-on-sso-to-multiple-applications-64637da015f4

