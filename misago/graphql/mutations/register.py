from ariadne import MutationType
from pydantic import EmailStr, create_model

from ...types import GraphQLContext
from ...users.create import create_user
from ...validation import (
    passwordstr,
    usernamestr,
    validate_data,
    validate_email_is_available,
    validate_model,
    validate_username_is_available,
)


register_mutation = MutationType()


@register_mutation.field("register")
async def resolve_register(_, info, *, input):  # pylint: disable=redefined-builtin
    # TODO:
    # add filter for create_input_model
    # add filter for cleaned_data
    # add filter for constructing data validators dict
    # add filter for create_user
    input_model = create_input_model(info.context)
    cleaned_data, errors = validate_model(input_model, input)

    errors = await validate_data(
        cleaned_data,
        {
            "name": [validate_username_is_available(),],
            "email": [validate_email_is_available()],
        },
        errors,
    )

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
