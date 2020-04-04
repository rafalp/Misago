from ariadne import MutationType
from graphql import GraphQLResolveInfo

from ....auth import authenticate_user, create_user_token
from ....errors import AllFieldsAreRequiredError, InvalidCredentialsError, NotAdminError
from ....hooks import authenticate_user_hook, create_user_token_hook
from ...errorhandler import error_handler


login_mutation = MutationType()


@login_mutation.field("login")
@error_handler
async def resolve_admin_login(
    _, info: GraphQLResolveInfo, *, username: str, password: str
):
    username = str(username or "").strip()
    password = str(password or "")

    if not username or not password:
        raise AllFieldsAreRequiredError()

    user = await authenticate_user_hook.call_action(
        authenticate_user, info.context, username, password, in_admin=True
    )

    if not user:
        raise InvalidCredentialsError()
    if not user.is_admin:
        raise NotAdminError()

    token = await create_user_token_hook.call_action(
        create_user_token, info.context, user, in_admin=True
    )
    return {"user": user, "token": token}
