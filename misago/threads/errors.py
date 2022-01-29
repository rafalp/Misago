from typing import Union

from pydantic import PydanticValueError

from ..validation import BaseError


class PostError(BaseError):
    base_name = "post_error"


class ThreadError(BaseError):
    base_name = "thread_error"


class PostNotAuthorError(PostError):
    code = "not_author"
    msg_template = "must be author of post with id '{id}'"

    def __init__(self, *, post_id: Union[int, str]) -> None:
        super().__init__(id=post_id)


class ThreadNotAuthorError(ThreadError):
    code = "not_author"
    msg_template = "must be author of thread with id '{id}'"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class PostNotFoundError(PostError):
    code = "not_found"
    msg_template = "post with id '{id}' could not be found"

    def __init__(self, *, post_id: Union[int, str]) -> None:
        super().__init__(id=post_id)


class ThreadNotFoundError(ThreadError):
    code = "not_found"
    msg_template = "thread with id '{id}' could not be found"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class PostIsThreadStartError(PostError):
    code = "thread_start"
    msg_template = "post with id '{id}' is thread's first post"

    def __init__(self, *, post_id: Union[int, str]) -> None:
        super().__init__(id=post_id)


class ThreadIsClosedError(ThreadError):
    code = "closed"
    msg_template = "thread with id '{id}' is closed"

    def __init__(self, *, thread_id: Union[int, str]) -> None:
        super().__init__(id=thread_id)


class ThreadTitleNotAllowedError(PydanticValueError):
    code = "thread_title.not_allowed"
    msg_template = "thread title is not allowed"
