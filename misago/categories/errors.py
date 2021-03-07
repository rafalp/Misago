from typing import Union

from pydantic import PydanticValueError


class CategoryInvalidError(PydanticValueError):
    code = "category.invalid"
    msg_template = "category '{id}' is invalid choice"

    def __init__(self, *, category_id: Union[int, str]) -> None:
        super().__init__(id=category_id)


class CategoryInvalidParentError(PydanticValueError):
    code = "category.invalid_parent"
    msg_template = "category can't have category '{id}' for parent category"

    def __init__(self, *, category_id: Union[int, str]) -> None:
        super().__init__(id=category_id)
