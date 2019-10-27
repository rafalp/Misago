from ariadne import MutationType

from ...passwords import verify_password
from ...user import get_user_by_name_or_email


login_mutation = MutationType()


@login_mutation.field("login")
async def resolve_login(_, info, *, username: str, password: str):
    username = username.strip()
    password = password.strip()

    if not username or not password:
        return {"error": "complete_form"}

    user = await get_user_by_name_or_email(username)
    if user and user["password"] and await verify_password(password, user["password"]):
        return {"user": user, "token": "not-implemented"}

    return {"error": "not_found"}
