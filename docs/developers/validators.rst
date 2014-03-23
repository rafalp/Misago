=================
Misago Validators
=================

Misago apps implement plenty of validators, someof which are considered public API. Those validators are documented here.


validate_sluggable
==================

:py:class:`misago.core.validators.validate_sluggable`

Callable class that validates if string can be converted to non-empty slug thats no longer than 255 characters.

To you use it, first instantiate it. If you want to define custom error messages, you can pass them using ``error_short`` and ``error_long`` arguments on initializer. After that you can simply call the class like other validator functions to see if it raises ``ValidationError``::

    from misago.core.validators import validate_sluggable
    validator = validate_sluggable()
    validator(some_value)
