from typing import Dict, List, Optional, Type, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, EmailStr, PositiveInt, constr, create_model

from ....context import Context
from ....users.errors import (
    UserDeactivateSelfError,
    UserIsProtectedError,
    UserRemoveOwnAdminError,
)
from ....users.loaders import users_loader
from ....users.models import User
from ....users.validators import (
    EmailIsAvailableValidator,
    UserExistsValidator,
    UsernameIsAvailableValidator,
    passwordstr,
    usernamestr,
)
from ....validation import Validator, validate_data, validate_model
from ...errorhandler import error_handler
from ..decorators import admin_resolver

user_update_mutation = MutationType()


@user_update_mutation.field("userUpdate")
@admin_resolver
@error_handler
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

    user_obj: Optional[User] = cleaned_data.pop("user", None)

    if user_obj:
        validators: Dict[str, List[Validator]] = {
            "name": [
                UsernameIsAvailableValidator(user_obj.id),
            ],
            "email": [
                EmailIsAvailableValidator(user_obj.id),
            ],
            "is_active": [is_active_validator(info.context, user_obj)],
            "is_admin": [is_admin_validator(info.context, user_obj)],
        }
        cleaned_data, errors = await validate_data(cleaned_data, validators, errors)

    if errors:
        return {"errors": errors, "updated": False, "user": user_obj}

    if user_obj and cleaned_data:
        updated_user = await update_user(info.context, user_obj, cleaned_data)
        return {"updated": updated_user != user_obj, "user": updated_user}

    return {"updated": False, "user": user}


def create_input_model(context: Context) -> Type[BaseModel]:
    return create_model(
        "UserCreateInputModel",
        user=(PositiveInt, ...),
        name=(usernamestr(context["settings"]), None),
        full_name=(constr(strip_whitespace=True, max_length=50), None),
        email=(EmailStr, None),
        password=(passwordstr(context["settings"]), None),
        is_active=(bool, None),
        is_moderator=(bool, None),
        is_admin=(bool, None),
    )


def is_active_validator(context: Context, user: User):
    async def validate_is_active(is_active: bool, errors, field_name):
        if is_active is False:
            context_user = cast(User, context["user"])
            if user.id == context_user.id:
                raise UserDeactivateSelfError()
            if user.is_admin:
                raise UserIsProtectedError(user_id=user.id)

        return is_active

    return validate_is_active


def is_admin_validator(context: Context, user: User):
    async def validate_is_admin(is_admin: bool, errors, field_name):
        context_user = cast(User, context["user"])
        if is_admin is False and user.id == context_user.id:
            raise UserRemoveOwnAdminError(user_id=user.id)

        return is_admin

    return validate_is_admin


async def update_user(context: Context, user: User, cleaned_data: dict) -> User:
    user = await user.update(**cleaned_data)
    users_loader.store(context, user)
    return user
