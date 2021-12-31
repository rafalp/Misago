from typing import Dict, List, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, EmailStr, create_model

from ....loaders import store_user
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
from ..decorators import admin_resolver

user_create_mutation = MutationType()


@user_create_mutation.field("userCreate")
@admin_resolver
@error_handler
@convert_kwargs_to_snake_case
async def resolve_user_create(
    _,
    info: GraphQLResolveInfo,
    *,
    input: dict,  # pylint: disable=redefined-builtin
):
    input_model = create_input_model(info.context)
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
        cleaned_data, errors = await validate_data(cleaned_data, validators, errors)

    if errors:
        return {"errors": errors}

    user = await register_user(info.context, cleaned_data)

    return {"user": user}


def create_input_model(context: GraphQLContext) -> Type[BaseModel]:
    return create_model(
        "UserCreateInputModel",
        name=(usernamestr(context["settings"]), ...),
        email=(EmailStr, ...),
        password=(passwordstr(context["settings"]), ...),
    )


async def register_user(context: GraphQLContext, cleaned_data: dict) -> User:
    def create_user(*args, **kwargs):
        return User.create(*args, **kwargs)

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
