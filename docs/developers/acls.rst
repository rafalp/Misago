====
ACLs
====


Extending permissions system
============================


Algebra
-------

Consider those three simple ACLs::

    acls = (
        {'can_be_knight': False},
        {'can_be_knight': True},
        {'can_be_knight': False},
    )

In order to obtain final ACL, one or more ACLs have to be sum together. Such operation requires loop over ACLs which compares values of dicts keys and picks preffered ones.

This problem can be solved using simple implementation::

    final_acl = {'can_be_knight': False}

    for acl in acls:
        if acl['can_be_knight']:
            final_acl['can_be_knight'] = True

But what if there are 20 permissions in ACL? Or if we are comparing numbers? What if complex rules are involved like popular "greater beats lower, zero beats all" in comparisions? This brings need for more suffisticated solution and Misago provides one in forum of ``misago.acl.algebra`` module.

This module provides utilities for summing two acls and supports three most common comparisions found in web apps:

* **greater**: True beats False, 42 beats 13
* **lower**: False beats True, 13 beats 42
* **greater or zero**: 42 beats 13, zero beats everything


.. function:: sum_acls(defaults, *acls, **permissions)

This function sums ACLs provided as ``*args`` using callables accepting two arguments defined in kwargs used to compare permission values. Example usage is following::

    from misago.acl import algebra

    user_acls = [
        {
            'can_see': False,
            'can_hear': False,
            'max_speed': 10,
            'min_age': 16,
            'speed_limit': 50,
        },
        {
            'can_see': True,
            'can_hear': False,
            'max_speed': 40,
            'min_age': 20,
            'speed_limit': 0,
        },
        {
            'can_see': False,
            'can_hear': True,
            'max_speed': 80,
            'min_age': 18,
            'speed_limit': 40,
        },
    ]

    defaults = {
        'can_see': False,
        'can_hear': False,
        'max_speed': 30,
        'min_age': 18,
        'speed_limit': 60,
    }

    final_acl = algebra.sum_acls(
        defaults, *user_acls,
        can_see=algebra.greater,
        can_hear=algebra.greater,
        max_speed=algebra.greater,
        min_age=algebra.lower,
        speed_limit=algebra.greater_or_zero
        )

As you can see because tests are callables, its easy to extend ``sum_acls`` support for new tests specific for your ACLs.
