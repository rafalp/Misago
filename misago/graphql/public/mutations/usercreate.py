from typing import Any, Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import EmailStr, create_model

from ....auth import create_user_token
from ....errors import ErrorsList
from ....loaders import store_user
from ....users.create import create_user
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
from .hooks.usercreate import (
    UserCreateInput,
    UserCreateInputModel,
    user_create_hook,
    user_create_input_hook,
    user_create_input_model_hook,
)

user_create_mutation = MutationType()


@user_create_mutation.field("userCreate")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_user_create(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await user_create_input_model_hook.call_action(
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
        cleaned_data, errors = await user_create_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors}

    user = await user_create_hook.call_action(register_user, info.context, cleaned_data)
    token = await create_user_token(info.context, user, in_admin=False)

    return {"user": user, "token": token}


async def create_input_model(context: GraphQLContext) -> UserCreateInputModel:
    return create_model(
        "RegisterInputModel",
        name=(usernamestr(context["settings"]), ...),
        email=(EmailStr, ...),
        password=(passwordstr(context["settings"]), ...),
        captcha=(Any, None),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: UserCreateInput,
    errors: ErrorsList,
) -> Tuple[UserCreateInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def register_user(context: GraphQLContext, cleaned_data: UserCreateInput) -> User:
    user = await create_user(
        cleaned_data["name"],
        cleaned_data["email"],
        password=cleaned_data["password"],
        context=context,
    )
    store_user(context, user)
    return user
