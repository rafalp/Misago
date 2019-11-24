from ariadne import MutationType
from pydantic import BaseModel, EmailStr, constr

from ...users.create import create_user
from ...validation import validate_model


register_mutation = MutationType()


@register_mutation.field("register")
async def resolve_register(_, info, *, input):  # pylint: disable=redefined-builtin
    cleaned_data, errors = validate_model(RegisterModel, input)

    if not errors:
        return {
            "user": await create_user(
                cleaned_data["name"],
                cleaned_data["email"],
                password=cleaned_data["password"],
            )
        }

    return {"errors": errors, "user": cleaned_data}


class RegisterModel(BaseModel):
    name: constr(strip_whitespace=True)  # type: ignore
    email: EmailStr()  # type: ignore
    password: str
