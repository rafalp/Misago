from typing import Union

from pydantic import PydanticValueError


class EmailNotAvailableError(PydanticValueError):
    code = "email.not_available"
    msg_template = "e-mail is not available"


class UserDeleteSelfError(PydanticValueError):
    code = "user.delete_self"
    msg_template = "user can't delete own account"


class UserDeactivateSelfError(PydanticValueError):
    code = "user.deactivate_self"
    msg_template = "user can't deactivate own account"


class UserIsProtectedError(PydanticValueError):
    code = "user.is_protected"
    msg_template = "user with id '{id}' is protected"

    def __init__(self, *, user_id: Union[int, str]) -> None:
        super().__init__(id=user_id)


class UserRemoveOwnAdminError(PydanticValueError):
    code = "user.remove_own_admin"
    msg_template = "user can't remove own admin status"


class UserNotFoundError(PydanticValueError):
    code = "user.not_found"
    msg_template = "user with id '{id}' could not be found"

    def __init__(self, *, user_id: Union[int, str]) -> None:
        super().__init__(id=user_id)


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
