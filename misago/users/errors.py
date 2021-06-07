from typing import Union

from pydantic import PydanticValueError


class CantDeleteSelfError(PydanticValueError):
    code = "user.delete_self"
    msg_template = "authenticated user can't delete themselves"


class UserIsProtectedError(PydanticValueError):
    code = "user.is_protected"
    msg_template = "user with id '{id}' is protected"

    def __init__(self, *, user_id: Union[int, str]) -> None:
        super().__init__(id=user_id)
