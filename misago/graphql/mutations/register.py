from typing import Union

from ariadne import MutationType
from pydantic import EmailStr, create_model, constr

from ...types import GraphQLContext
from ...users.create import create_user
from ...validation import validate_data, validate_model
from ...validation.constraints import passwordstr, usernamestr


register_mutation = MutationType()


@register_mutation.field("register")
async def resolve_register(_, info, *, input):  # pylint: disable=redefined-builtin
    input_model = create_input_model(info.context)
    cleaned_data, errors = validate_model(input_model, input)

    errors += await validate_data(cleaned_data, {"name": [], "email": [],})

    if errors:
        return {"errors": errors}

    return {
        "user": await create_user(
            cleaned_data["name"],
            cleaned_data["email"],
            password=cleaned_data["password"],
        )
    }


def create_input_model(context: GraphQLContext):
    return create_model(
        "RegisterInput",
        name=(usernamestr(context["settings"]), ...),
        email=(EmailStr, ...),
        password=(passwordstr(context["settings"]), ...),
    )
