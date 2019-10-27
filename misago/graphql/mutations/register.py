from ariadne import MutationType
from pydantic import EmailStr, ValidationError, constr, create_model

from ...user import create_user


register_mutation = MutationType()


@register_mutation.field("register")
async def resolve_register(_, info, *, input):  # pylint: disable=redefined-builtin
    InputModel = create_registration_model()
    try:
        data = InputModel(**input).dict()
    except ValidationError as e:
        return {"errors": e.errors()}

    user = await create_user(data["name"], data["email"], password=data["password"])
    return {"user": user}


def create_registration_model():
    return create_model(
        "RegisterModel",
        name=(constr(min_length=1, max_length=15, strip_whitespace=True), ...),
        email=EmailStr(),
        password=(constr(min_length=1, max_length=40, strip_whitespace=False), ...),
    )
