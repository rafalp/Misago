=============
Sending Mails
=============


Misago provides its own API for sending e-mails to forum users that extends standard `Django mailer <https://docs.djangoproject.com/en/dev/topics/email/>`_.

This API lives in :py:mod:`misago.core.mail` and has two functions:


mail_user
---------

.. function:: mail_user(request, recipient, subject, template, context=None)

Build e-mail message using supplied template name and (optionally context), then send it to user. Template name shouldn't contain file extension, as Misago will automatically append ``.html`` for html content and ``.txt`` for plaintext content for sent message. Message templates will have access to same request context as other templates, additional context you've provided and two extra context values: ``recipient`` and ``sender``.

* ``request:`` HttpRequest object instance.
* ``recipient:`` User model instance.
* ``subject:`` A string.
* ``template:`` A string.
* ``context:`` The optional dictionary with extra context values that should be available for message templates.


mail_users
----------

.. function:: mail_users(request, recipients, subject, template, context=None)

Same as above, but instead of sending message to one recipient, it sends it to many recipients at same time. Keep on mind this may be memory intensitive as this function creates one Mail object instance for every recipient specified, so you may want to split recipients into smaller groups as you are sending them emails.

* ``recipients:`` Iterable of User models.
