from typing import Optional, cast

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt

from ...context import Context
from ...users.delete import delete_user, delete_user_content
from ...users.errors import UserDeleteSelfError, UserIsProtectedError
from ...users.loaders import users_loader
from ...users.models import User
from ...users.validators import UserExistsValidator
from ...validation import validate_data, validate_model
from ..mutation import AdminMutationType, ErrorType


class AdminUserDeleteResultType(ObjectType):
    __schema__ = gql(
        """
        type UserDeleteResult {
            deleted: Boolean!
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType]


class AdminUserDeleteMutation(AdminMutationType):
    __schema__ = gql(
        """
        type Mutation {
            userDelete(user: ID!, deleteContent: Boolean): UserDeleteResult!
        }
        """
    )
    __args__ = {
        "deleteContent": "delete_content",
    }
    __requires__ = [AdminUserDeleteResultType]

    @classmethod
    async def mutate(  # type: ignore
        cls,
        info: GraphQLResolveInfo,
        *,
        user: str,
        delete_content: Optional[bool] = False,
    ):
        cleaned_data, errors = await cls.clean_data(
            info,
            {
                "user": user,
                "delete_content": delete_content,
            },
        )

        if errors:
            return {"errors": errors, "deleted": False}

        user_obj = cleaned_data["user"]

        if delete_content:
            await delete_user_content(user_obj)

        await delete_user(user_obj)
        users_loader.unload(info.context, user_obj.id)

        return {"deleted": True}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        cleaned_data, errors = validate_model(DeleteUserInputModel, data)
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
        return cleaned_data, errors


class DeleteUserInputModel(BaseModel):  # type: ignore
    user: PositiveInt
    delete_content: bool


def user_can_be_deleted_validator(context: Context):
    async def validate_delete_user(user: User, errors, field_name):
        context_user = cast(User, context["user"])
        if user.id == context_user.id:
            raise UserDeleteSelfError()
        if user.is_admin:
            raise UserIsProtectedError(user_id=user.id)

        return user

    return validate_delete_user
