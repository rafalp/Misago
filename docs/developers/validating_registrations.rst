========================
Validating Registrations
========================

Misago implements simple framework for extending process of new user registration with additional checks.

When user submits registration form with valid data, this data is then passed to functions defined in `MISAGO_NEW_REGISTRATIONS_VALIDATORS` setting.

Each function is called with following arguments:

* ``ip:`` IP address using form.
* ``username:`` username for which new account will be created.
* ``email:`` e-mail address for which new account will be created.

If function decides to interrup registration process and thus stop user from registering account, it can raise `django.core.exceptions.PermissionDenied` exception, which will result in user receiving "403 Permission Denied" response from site, as well as having his IP address automatically banned for one day.

If none of defined tests raised `PermissionDenied`, user account will be registered normally.
