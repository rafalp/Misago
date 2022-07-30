from typing import Union

from ..validation import BaseError


class CategoryError(BaseError):
    base_name = "category_error"


class CategoryNotFoundError(CategoryError):
    code = "not_found"
    msg_template = "category with id '{id}' could not be found"

    def __init__(self, *, category_id: Union[int, str]) -> None:
        super().__init__(id=category_id)  # type: ignore


class CategoryIsClosedError(CategoryError):
    code = "closed"
    msg_template = "category with id '{id}' is closed"

    def __init__(self, *, category_id: Union[int, str]) -> None:
        super().__init__(id=category_id)  # type: ignore


class CategoryInvalidError(CategoryError):
    code = "invalid"
    msg_template = "category '{id}' is invalid choice"

    def __init__(self, *, category_id: Union[int, str]) -> None:
        super().__init__(id=category_id)  # type: ignore


class CategoryInvalidParentError(CategoryError):
    code = "invalid_parent"
    msg_template = "category can't have category '{id}' as parent category"

    def __init__(self, *, category_id: Union[int, str]) -> None:
        super().__init__(id=category_id)  # type: ignore
