from typing import Union

from pydantic import PydanticValueError


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
