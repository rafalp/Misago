from ariadne import MutationType
from graphql import GraphQLResolveInfo

from ....auth import authenticate_user, create_user_token
from ....auth.hooks import authenticate_user_hook, create_user_token_hook
from ....errors import AllFieldsAreRequiredError, InvalidCredentialsError
from ...errorhandler import error_handler

login_mutation = MutationType()


@login_mutation.field("login")
@error_handler
async def resolve_login(_, info: GraphQLResolveInfo, *, username: str, password: str):
    username = str(username or "").strip()
    password = str(password or "")

    if not username or not password:
        raise AllFieldsAreRequiredError()

    user = await authenticate_user_hook.call_action(
        authenticate_user, info.context, username, password, in_admin=False
    )

    if not user:
        raise InvalidCredentialsError()

    token = await create_user_token_hook.call_action(
        create_user_token, info.context, user, in_admin=False
    )
    return {"user": user, "token": token}
