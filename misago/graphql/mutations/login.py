from ariadne import MutationType

from ...user import get_user_by_name_or_email


login_mutation = MutationType()


@login_mutation.field("login")
async def resolve_login(_, info, *, username: str, password: str):
    username = username.strip()
    password = password.strip()

    user = await get_user_by_name_or_email(username)
    if user and user["password"] == password:
        return {"user": user}

    return {"error": "NOT_FOUND"}
