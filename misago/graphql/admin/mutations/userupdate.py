from typing import Dict, List, Optional, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, EmailStr, PositiveInt, constr, create_model

from ....loaders import store_user
from ....users.hooks.updateuser import update_user_hook
from ....users.models import User
from ....validation import (
    EmailIsAvailableValidator,
    UserExistsValidator,
    UsernameIsAvailableValidator,
    Validator,
    passwordstr,
    usernamestr,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from ..decorators import admin_mutation

user_update_mutation = MutationType()


@user_update_mutation.field("userUpdate")
@error_handler
@admin_mutation
@convert_kwargs_to_snake_case
async def resolve_user_update(
    _,
    info: GraphQLResolveInfo,
    *,
    user: str,
    input: dict,  # pylint: disable=redefined-builtin
):
    input["user"] = user

    input_model = create_input_model(info.context)
    cleaned_data, errors = validate_model(input_model, input)
    cleaned_data, errors = await validate_data(
        cleaned_data,
        {
            "user": [
                UserExistsValidator(info.context),
            ],
        },
        errors,
    )

    user: Optional[User] = cleaned_data.pop("user", None)

    if user:
        validators: Dict[str, List[Validator]] = {
            "name": [
                UsernameIsAvailableValidator(user.id),
            ],
            "email": [
                EmailIsAvailableValidator(user.id),
            ],
        }
        cleaned_data, errors = await validate_data(cleaned_data, validators, errors)

    if errors:
        return {"errors": errors, "updated": False}

    if user and cleaned_data:
        updated_user = await update_user(info.context, user, cleaned_data)
        return {"updated": updated_user != user, "user": updated_user}

    return {"updated": False, "user": user}


def create_input_model(context: GraphQLContext) -> Type[BaseModel]:
    return create_model(
        "UserCreateInputModel",
        user=(PositiveInt, ...),
        name=(usernamestr(context["settings"]), None),
        full_name=(constr(strip_whitespace=True, max_length=50), None),
        email=(EmailStr, None),
        password=(passwordstr(context["settings"]), None),
        is_active=(bool, None),
        is_moderator=(bool, None),
        is_administrator=(bool, None),
    )


async def update_user(context: GraphQLContext, user: User, cleaned_data: dict) -> User:
    def update_user_action(user: User, context=None, **cleaned_data):
        return user.update(**cleaned_data)

    user = await update_user_hook.call_action(
        update_user_action,
        user,
        context=context,
        **cleaned_data,
    )
    store_user(context, user)
    return user
