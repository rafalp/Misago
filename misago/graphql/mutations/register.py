from typing import Any, Dict, List, Tuple, Union

from ariadne import MutationType
from pydantic import EmailStr, create_model

from ...hooks import register_input_hook, register_input_model_hook
from ...types import (
    AsyncRootValidator,
    AsyncValidator,
    GraphQLContext,
    RegisterInputModel,
)
from ...users.create import create_user
from ...validation import (
    ErrorsList,
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
    input_model = await register_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data:
        validators = {
            "name": [validate_username_is_available(),],
            "email": [validate_email_is_available()],
        }
        cleaned_data, errors = await register_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
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


async def create_input_model(context: GraphQLContext) -> RegisterInputModel:
    return create_model(
        "RegisterInput",
        name=(usernamestr(context["settings"]), ...),
        email=(EmailStr, ...),
        password=(passwordstr(context["settings"]), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Union[AsyncRootValidator, AsyncValidator]]],
    cleaned_data: Dict[str, Any],
    errors: ErrorsList,
) -> Tuple[Dict[str, Any], ErrorsList]:
    errors = await validate_data(cleaned_data, validators, errors)
    return cleaned_data, errors
