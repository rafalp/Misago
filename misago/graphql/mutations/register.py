from ariadne import MutationType

from ...user import create_user


register_mutation = MutationType()


@register_mutation.field("register")
async def resolve_register(_, info, *, input):
    user = await create_user(input["name"], input["email"], password=input["password"])
    return {"user": user}
