from typing import Dict, List, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, EmailStr, create_model

from ....context import Context
from ....users.create import create_user
from ....users.loaders import users_loader
from ....users.models import User
from ....users.validators import (
    EmailIsAvailableValidator,
    UsernameIsAvailableValidator,
    passwordstr,
    usernamestr,
)
from ....validation import Validator, validate_data, validate_model
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


def create_input_model(context: Context) -> Type[BaseModel]:
    return create_model(
        "UserCreateInputModel",
        name=(usernamestr(context["settings"]), ...),
        email=(EmailStr, ...),
        password=(passwordstr(context["settings"]), ...),
    )


async def register_user(context: Context, cleaned_data: dict) -> User:
    user = await create_user(
        context,
        cleaned_data["name"],
        cleaned_data["email"],
        password=cleaned_data["password"],
    )
    users_loader.store(context, user)
    return user