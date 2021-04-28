from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import EmailStr, create_model

from ....auth import create_user_token
from ....auth.hooks import create_user_token_hook
from ....errors import ErrorsList
from ....loaders import store_user
from ....users.create import create_user
from ....users.hooks import create_user_hook
from ....users.models import User
from ....validation import (
    EmailIsAvailableValidator,
    UsernameIsAvailableValidator,
    Validator,
    passwordstr,
    usernamestr,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.registeruser import (
    RegisterUserInput,
    RegisterUserInputModel,
    register_user_hook,
    register_user_input_hook,
    register_user_input_model_hook,
)

register_mutation = MutationType()


@register_mutation.field("register")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_register(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await register_user_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "name": [
                UsernameIsAvailableValidator(),
            ],
            "email": [
                EmailIsAvailableValidator(),
            ],
        }
        cleaned_data, errors = await register_user_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors}

    user = await register_user_hook.call_action(
        register_user, info.context, cleaned_data
    )
    token = await create_user_token_hook.call_action(
        create_user_token, info.context, user, in_admin=False
    )

    return {"user": user, "token": token}


async def create_input_model(context: GraphQLContext) -> RegisterUserInputModel:
    return create_model(
        "RegisterInputModel",
        name=(usernamestr(context["settings"]), ...),
        email=(EmailStr, ...),
        password=(passwordstr(context["settings"]), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: RegisterUserInput,
    errors: ErrorsList,
) -> Tuple[RegisterUserInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def register_user(
    context: GraphQLContext, cleaned_data: RegisterUserInput
) -> User:
    user = await create_user_hook.call_action(
        create_user,
        cleaned_data["name"],
        cleaned_data["email"],
        password=cleaned_data["password"],
        extra={},
        context=context,
    )
    store_user(context, user)
    return user
