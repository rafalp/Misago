from typing import Any, Dict, Union

from ariadne import MutationType
from pydantic import PydanticTypeError, PydanticValueError

from ...auth import authenticate_user, create_user_token
from ...hooks import authenticate_user_hook, create_user_token_hook
from ...validation.errors import AllFieldsAreRequiredError, InvalidCredentialsError
from ...validation.errorslist import get_error_type


def handle_login_errors(f):
    async def wrapped_login_mutation(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except (AllFieldsAreRequiredError, InvalidCredentialsError) as e:
            return {"error": {"msg": str(e), "type": get_error_type(e),}}

    return wrapped_login_mutation


login_mutation = MutationType()


@login_mutation.field("login")
async def resolve_login(_, info, *, username: str, password: str):
    username = str(username or "").strip()
    password = str(password or "")

    if not username or not password:
        return return_error(AllFieldsAreRequiredError())

    try:
        user = await authenticate_user_hook.call_action(
            authenticate_user, info.context, username, password
        )

        if not user:
            return return_error(InvalidCredentialsError())
    except (PydanticTypeError, PydanticValueError) as error:
        return return_error(error)

    token = await create_user_token_hook.call_action(
        create_user_token, info.context, user
    )
    return {"user": user, "token": token}


def return_error(error: Union[PydanticTypeError, PydanticValueError]) -> Dict[str, Any]:
    return {"error": {"msg": str(error), "type": get_error_type(error),}}
