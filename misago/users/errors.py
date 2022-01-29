from typing import Union

from pydantic.errors import PydanticValueError

from ..validation import BaseError


class EmailNotAvailableError(PydanticValueError):
    code = "email.not_available"
    msg_template = "e-mail is not available"


class UsernameError(PydanticValueError):
    code = "username"
    msg_template = 'username does not match regex "{pattern}"'

    def __init__(  # pylint: disable=useless-super-delegation
        self, *, pattern: str
    ) -> None:
        super().__init__(pattern=pattern)


class UsernameNotAvailableError(PydanticValueError):
    code = "username.not_available"
    msg_template = "username is not available"


class UsernameNotAllowedError(PydanticValueError):
    code = "username.not_allowed"
    msg_template = "username is not allowed"


class UserError(BaseError):
    base_name = "user_error"


class UserNotFoundError(UserError):
    code = "not_found"
    msg_template = "user with id '{id}' could not be found"

    def __init__(self, *, user_id: Union[int, str]) -> None:
        super().__init__(id=user_id)


class UserDeleteSelfError(UserError):
    code = "delete_self"
    msg_template = "user can't delete own account"


class UserDeactivateSelfError(UserError):
    code = "deactivate_self"
    msg_template = "user can't deactivate own account"


class UserIsProtectedError(UserError):
    code = "is_protected"
    msg_template = "user with id '{id}' is protected"

    def __init__(self, *, user_id: Union[int, str]) -> None:
        super().__init__(id=user_id)


class UserRemoveOwnAdminError(UserError):
    code = "remove_own_admin"
    msg_template = "user can't remove own admin status"
