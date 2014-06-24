=====================
Permissions framework
=====================

Misago brings its own ACL (Access Control Lists) framework for implementing permissions and this document explains to how to use and extend it with your own permissions.


Checking permissions
====================

Permissions are stored on special models named "roles" and assigned to users either directly or trough ranks. Guest users always have permissions from "Guest" role, and users always have permissions form "Member" role.

There are two kinds of objects in Misago: aware and unaware of their ACL's. Aware objects have "acl" attribute containing dict with their permissions for given ACL, while unaware objects don't. Instances of ``User`` and ``AnonymousUser`` classes are always ACL aware, while other objects need you to make them aware of their ACLs through use of ``add_acl`` functions ofered by ``misago.acl`` module. However this is not always needed (or possible), in which cases you have to introspect user's acl attribute directly.

ACL's are simple dictionaries, and their contents differ depending on objects they are belonging to. This means that to see if forum is visible to user, you have to perform following check::

    if user.acl['forums'].get(forum.pk, {}).get('can_see'):
        # huzza, we can see forum!

Above snippet is edge example of checking forum permission, and luckily we have few alternatives::

    if forum.pk in userl.acl['visible_forums']:
        # Not really shorter, but simpler to remember and works in django templates!

    from misago.acl import add_acl

    add_acl(user, forums)
    for forum in forums
        if forum.acl['can_see']:
            # Now model instances in forums queryset are aware of their ACLs!
            # ACL's are easy to check in templates too now!

Because ACL framework is very flexible, different features can have different ways to check their permissions.


Permissions cache
-----------------

Construction of User's ACLs can be costful process, especially once you start installing extensions adding new features to your site. Because of this, Misago is not assinging ACLs to Users, but to combinations of roles.

This means that if one User has roles 1, 3 and 4 assigned to account, but no rank, while other User has roles 1 and 4 assigned to account and role 3 assigned to his rank, both will have same ACL. This means that ACL has to be generated once and cached for use by others.

ACL's are cached in two places: in remote cache storage, for use between requests, and in thread memory, so you don't have to write your own caches and checks when you are checking multiple users ACL's during single request.

ACL cache is versioned and rebuilded when cache version is different than current ACL version, which happens when models being part of ACL framework are edited or deleted.


Extending permissions system
============================

ACL framework extensions are modules registered in ``MISAGO_ACL_EXTENSIONS`` setting. By convention, those modules are either named "permissions", or they are located in "permissions" package.

Misago checks module for following functions:


.. function:: change_permissions_form(role)

Required. This function is called when change permissions form for role is being build for view. It's expected to return Form type or none, if provider is not recognizing role type (eg. there is no sense in adding profiles visibility permissions to forums role form).

.. note::
   Misago provides custom ``YesNoSwitch`` form field that renders nice "Yes/No" switch as input. This field is simple wrapper around ``TypedChoiceField`` that coerces to ``int``. If you use use it for your permissions, make sure your ACL implementation handles their values as ``1`` or ``0``, not as ``True`` or ``False``, or your forms will break!

.. warning::
   Make sure that all fields in your form have initial value, or your form will make tests suite fail because it will be unable to mock POST requests to admin forms correctly.


.. function:: build_acl(acl, roles, key_name)

Required. Is used in process of building new ACL. Its supplied dict with incomplete ACL, list of user roles and name of key under which its permissions values are stored in roles ``permissions`` attributes. Its expected to access roles ``permissions`` attributes which are dicts of values coming from permission change forms and return updated ``acl`` dict.


.. function:: add_acl_to_target(user, acl, target)

Optional. Is called when Misago is trying to make ``target`` aware of its ACLs. Its provided with three arguments:

* **user** - user asking to make target aware of its ACL's
* **acl** - user ACLs
* **target** - target instance, guaranteed to be an single object, not list or other iterable (like queryset)

Value of ``target`` argument has ``acl`` attribute which is dict with incomplete ACL that function can change and update with new keys.

Misago comes with its own debug page titled "Misago User ACL" that is available from Django Debug Toolbar menu. This page display user roles permissions as well as final ACL assigned to current user.


Algebra
-------

Consider those three simple permission sets::

    roles_permissions = (
        {'can_be_knight': False},
        {'can_be_knight': True},
        {'can_be_knight': False},
    )

In order to obtain final ACL, one or more ACLs have to be sum together. Such operation requires loop over ACLs which compares values of dicts keys and picks preffered ones.

This problem can be solved using simple implementation::

    final_acl = {'can_be_knight': False}

    for acl in roles_permissions:
        if acl['can_be_knight']:
            final_acl['can_be_knight'] = True

But what if there are 20 permissions in ACL? Or if we are comparing numbers? What if complex rules are involved like popular "greater beats lower, zero beats all" in comparisions? This brings need for more suffisticated solution and Misago provides one in forum of ``misago.acl.algebra`` module.

This module provides utilities for summing two acls and supports three most common comparisions found in web apps:

* **greater**: True beats False, 42 beats 13
* **lower**: False beats True, 13 beats 42
* **greater or zero**: 42 beats 13, zero beats everything


.. function:: sum_acls(result_acl, acls=None, roles=None, key=None, **permissions)

This function adds ACLs to result_acl using set or rules provided as additional kwargs. Alternatively, it access iterable of roles and extension key.

Example usage is following::

    from misago.acl import algebra

    user_acls = [
        {
            'can_see': 0,
            'can_hear': 0,
            'max_speed': 10,
            'min_age': 16,
            'speed_limit': 50,
        },
        {
            'can_see': 1,
            'can_hear': 0,
            'max_speed': 40,
            'min_age': 20,
            'speed_limit': 0,
        },
        {
            'can_see': 0,
            'can_hear': 1,
            'max_speed': 80,
            'min_age': 18,
            'speed_limit': 40,
        },
    ]

    defaults = {
        'can_see': 0,
        'can_hear': 0,
        'max_speed': 30,
        'min_age': 18,
        'speed_limit': 60,
    }

    final_acl = algebra.sum_acls(
        defaults, acls=user_acls,
        can_see=algebra.greater,
        can_hear=algebra.greater,
        max_speed=algebra.greater,
        min_age=algebra.lower,
        speed_limit=algebra.greater_or_zero
        )

As you can see because tests are callables, its easy to extend ``sum_acls`` support for new tests specific for your ACLs.
