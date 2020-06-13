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
    code = "category.not_exists"
    msg_template = "category with id '{id}' does not exist"

    def __init__(self, *, category_id: Union[int, str]) -> None:
        super().__init__(id=category_id)


class CategoryClosedError(AuthError):
    code = "category.closed"
    msg_template = "category with id '{id}' is closed"

    def __init__(self, *, category_id: Union[int, str]) -> None:
        super().__init__(id=category_id)


class NotAuthorizedError(AuthError):
    code = "not_authorized"
    msg_template = "authorization is required"


class NotAdminError(AuthError):
    code = "not_admin"
    msg_template = "administrator permission is required"


class NotModeratorError(AuthError):
    code = "not_moderator"
    msg_template = "moderator permission is required"


class EmailNotAvailableError(PydanticValueError):
    code = "email.not_available"
    msg_template = "e-mail is not available"


class InvalidCredentialsError(PydanticValueError):
    code = "invalid_credentials"
    msg_template = "invalid credentials"


class ListRepeatedItemsError(PydanticValueError):
    code = "list.repeated_items"
    msg_template = "ensure all items of the list are unique"


class NotPostAuthorError(AuthError):
    code = "post.not_author"
    msg_template = "must be author of post with id '{id}'"

    def __init__(self, *, post_id: Union[int, str]) -> None:
        super().__init__(id=post_id)


class NotThreadAuthorError(AuthError):
    code = "thread.not_author"
    msg_template = "must be author of thread with id '{id}'"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class PostDoesNotExistError(PydanticValueError):
    code = "post.not_exists"
    msg_template = "post with id '{id}' does not exist"

    def __init__(self, *, post_id: Union[int, str]) -> None:
        super().__init__(id=post_id)


class ThreadDoesNotExistError(PydanticValueError):
    code = "thread.not_exists"
    msg_template = "thread with id '{id}' does not exist"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class ThreadFirstPostError(PydanticValueError):
    code = "post.thread_start"
    msg_template = "post with id '{id}' is thread's first post"

    def __init__(self, *, post_id: Union[int, str]) -> None:
        super().__init__(id=post_id)


class ThreadClosedError(AuthError):
    code = "thread.closed"
    msg_template = "thread with id '{id}' is closed"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class ThreadTitleNotAllowedError(PydanticValueError):
    code = "thread_title.not_allowed"
    msg_template = "thread title is not allowed"


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
