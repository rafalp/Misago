from typing import Dict, Union

from ariadne import MutationType
from pydantic import PydanticTypeError, PydanticValueError

from ...auth import authenticate_user, create_user_token
from ...hooks import authenticate_user_hook, create_user_token_hook
from ...types import Error
from ...validation import get_error_dict
from ...validation.errors import AllFieldsAreRequiredError, InvalidCredentialsError


login_mutation = MutationType()


@login_mutation.field("login")
async def resolve_login(_, info, *, username: str, password: str):
    username = str(username or "").strip()
    password = str(password or "")

    if not username or not password:
        return get_error_result(AllFieldsAreRequiredError())

    try:
        user = await authenticate_user_hook.call_action(
            authenticate_user, info.context, username, password
        )

        if not user:
            return get_error_result(InvalidCredentialsError())
    except (PydanticTypeError, PydanticValueError) as error:
        return get_error_result(error)

    token = await create_user_token_hook.call_action(
        create_user_token, info.context, user
    )
    return {"user": user, "token": token}


def get_error_result(
    error: Union[PydanticTypeError, PydanticValueError]
) -> Dict[str, Error]:
    return {"error": get_error_dict(error)}
