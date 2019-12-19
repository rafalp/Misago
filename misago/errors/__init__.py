from typing import Union

from pydantic import PydanticValueError

from .autherror import AuthError
from .errordict import ErrorDict
from .errorslist import ErrorsList
from .format import get_error_dict, get_error_type


class AllFieldsAreRequiredError(PydanticValueError):
    code = "all_fields_are_required"
    msg_template = "all fields are required"


class CategoryDoesNotExistError(PydanticValueError):
    code = "category_does_not_exist"
    msg_template = "category with id '{id}' does not exist"

    def __init__(self, *, category_id: Union[int, str]) -> None:
        super().__init__(id=category_id)


class CategoryIsClosedError(AuthError):
    code = "category_is_closed"
    msg_template = "category with id '{id}' is closed"

    def __init__(self, *, category_id: Union[int, str]) -> None:
        super().__init__(id=category_id)


class NotAuthorizedError(AuthError):
    code = "not_authorized"
    msg_template = "authorization is required"


class EmailIsNotAvailableError(PydanticValueError):
    code = "email.not_available"
    msg_template = "e-mail is not available"


class InvalidCredentialsError(PydanticValueError):
    code = "invalid_credentials"
    msg_template = "invalid credentials"


class PostDoesNotExistError(PydanticValueError):
    code = "post_does_not_exist"
    msg_template = "post with id '{id}' does not exist"

    def __init__(self, *, post_id: Union[int, str]) -> None:
        super().__init__(id=post_id)


class ThreadDoesNotExistError(PydanticValueError):
    code = "thread_does_not_exist"
    msg_template = "thread with id '{id}' does not exist"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class ThreadIsClosedError(AuthError):
    code = "thread_is_closed"
    msg_template = "thread with id '{id}' is closed"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class UsernameError(PydanticValueError):
    code = "username"
    msg_template = 'username does not match regex "{pattern}"'

    def __init__(  # pylint: disable=useless-super-delegation
        self, *, pattern: str
    ) -> None:
        super().__init__(pattern=pattern)


class UsernameIsNotAvailableError(PydanticValueError):
    code = "username.not_available"
    msg_template = "username is not available"
