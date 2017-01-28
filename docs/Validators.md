Validators
==========

Misago apps implement plenty of validators, some of which are considered public API. Those validators are per convention contained within `validators` module of their respective apps.


## `misago.core.validators.validate_sluggable`

Callable class that validates if string can be converted to non-empty slug thats no longer than 255 characters.

To you use it, first instantiate it. If you want to define custom error messages, you can pass them using `error_short` and `error_long` arguments on initializer. After that you can simply call the class like other validator functions to see if it raises `ValidationError`:

```python
from misago.core.validators import validate_sluggable
validator = validate_sluggable()
validator(some_value)
```


## `misago.users.validators`


### `validate_email.misago.users.validators.validate_email(value, exclude=None)`

Function that takes email address and runs content, availability and ban check validation in this order via calling dedicated validators. Optional `exclude` argument can be `User` instance to exclude from certain validation like uniqueness checks.


### `validate_email_banned.misago.users.validators.validate_email_banned(value)`

Function that accepts email string as its only argument and raises Validation error if it's banned.


### `validate_email_content.misago.users.validators.validate_email_content(value)`

Callable instance of `django.core.validators.EmailValidator` that checks if email address has valid structure and contents.


### `validate_password.misago.users.validators.validate_password(value)`

Function that takes plaintext password and runs length and complexity validation in this order via calling dedicated validators.


### `validate_password_complexity.misago.users.validators.validate_password_complexity(value)`

Validates password complexity against tests specified in `password_complexity` setting.


### `validate_password_length.misago.users.validators.validate_password_length(value)`

Validates password length and raises ValidationError if specified plaintext password is shorter than `password_length_min`.


### `validate_username.misago.users.validators.validate_username(value, exclude=None)`

Function that takes username and runs content, length, availability and ban check validation in this order via calling dedicated validators. Optional `exclude` argument can be `User` instance to exclude from certain validation like uniqueness checks.


### `validate_username_available.misago.users.validators.validate_username_available(value, exclude=None)`

Function that accepts username string as its only argument and raises ValidationError if it's already taken. Optional `exclude` argument can be `User` instance to exclude from certain validation like uniqueness checks.


### `validate_username_banned.misago.users.validators.validate_username_banned(value)`

Function that accepts username string as its only argument and raises Validation error if it's banned.


### `validate_username_content.misago.users.validators.validate_username_content(value)`

Function that accepts username string as its only argument and raises Validation error if username contains disallowed characters (eg. those that are not matched by `[0-9a-z]+` regex).


### `validate_username_length.misago.users.validators.validate_username_length(value)`

Function that accepts username string as its only argument and raises Validation error if it's shorter than `username_length_min` setting or longer than `username_length_max` setting.