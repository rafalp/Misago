from typing import Union

from pydantic import PydanticValueError

from .errordict import ErrorDict
from .errorslist import ErrorsList
from .format import get_error_dict, get_error_location, get_error_type


class AllFieldsAreRequiredError(PydanticValueError):
    code = "all_fields_are_required"
    msg_template = "all fields are required"


class ListRepeatedItemsError(PydanticValueError):
    code = "list.repeated_items"
    msg_template = "ensure all items of the list are unique"


class NotPostAuthorError(PydanticValueError):
    code = "post.not_author"
    msg_template = "must be author of post with id '{id}'"

    def __init__(self, *, post_id: Union[int, str]) -> None:
        super().__init__(id=post_id)


class NotThreadAuthorError(PydanticValueError):
    code = "thread.not_author"
    msg_template = "must be author of thread with id '{id}'"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class PostNotFoundError(PydanticValueError):
    code = "post.not_found"
    msg_template = "post with id '{id}' could not be found"

    def __init__(self, *, post_id: Union[int, str]) -> None:
        super().__init__(id=post_id)


class SiteWizardDisabledError(PydanticValueError):
    code = "site_wizard.disabled"
    msg_template = "site wizard is disabled"


class ThreadNotFoundError(PydanticValueError):
    code = "thread.not_found"
    msg_template = "thread with id '{id}' could not be found"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class ThreadFirstPostError(PydanticValueError):
    code = "post.thread_start"
    msg_template = "post with id '{id}' is thread's first post"

    def __init__(self, *, post_id: Union[int, str]) -> None:
        super().__init__(id=post_id)


class ThreadClosedError(PydanticValueError):
    code = "thread.closed"
    msg_template = "thread with id '{id}' is closed"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class ThreadTitleNotAllowedError(PydanticValueError):
    code = "thread_title.not_allowed"
    msg_template = "thread title is not allowed"
