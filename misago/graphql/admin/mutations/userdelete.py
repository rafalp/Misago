from typing import Optional, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt

from ....users.delete import delete_user, delete_user_content
from ....users.errors import UserDeleteSelfError, UserIsProtectedError
from ....users.loaders import users_loader
from ....users.models import User
from ....users.validators import UserExistsValidator
from ....validation import validate_data, validate_model
from ... import GraphQLContext
from ...errorhandler import error_handler
from ..decorators import admin_resolver

user_delete_mutation = MutationType()


@user_delete_mutation.field("userDelete")
@admin_resolver
@error_handler
@convert_kwargs_to_snake_case
async def resolve_user_delete(
    _,
    info: GraphQLResolveInfo,
    *,
    user: str,
    delete_content: Optional[bool] = False,
):
    input_data = {
        "user": user,
        "delete_content": delete_content,
    }

    cleaned_data, errors = validate_model(DeleteUserInputModel, input_data)
    cleaned_data, errors = await validate_data(
        cleaned_data,
        {
            "user": [
                UserExistsValidator(info.context),
                user_can_be_deleted_validator(info.context),
            ],
        },
        errors,
    )

    if errors:
        return {"errors": errors, "deleted": False}

    user_obj = cleaned_data["user"]

    if delete_content:
        await delete_user_content(user_obj)

    await delete_user(user_obj)
    users_loader.unload(info.context, user_obj.id)

    return {"deleted": True}


class DeleteUserInputModel(BaseModel):  # type: ignore
    user: PositiveInt
    delete_content: bool


def user_can_be_deleted_validator(context: GraphQLContext):
    async def validate_delete_user(user: User, errors, field_name):
        context_user = cast(User, context["user"])
        if user.id == context_user.id:
            raise UserDeleteSelfError()
        if user.is_admin:
            raise UserIsProtectedError(user_id=user.id)

        return user

    return validate_delete_user
