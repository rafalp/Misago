from typing import Dict, List, Optional, Type, cast

from ariadne_graphql_modules import InputType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, EmailStr, PositiveInt, constr, create_model

from ...context import Context
from ...users.errors import (
    UserDeactivateSelfError,
    UserIsProtectedError,
    UserRemoveOwnAdminError,
)
from ...users.loaders import users_loader
from ...users.models import User
from ...users.validators import (
    EmailIsAvailableValidator,
    UserExistsValidator,
    UsernameIsAvailableValidator,
    passwordstr,
    usernamestr,
)
from ...validation import Validator, validate_data, validate_model
from ..mutation import AdminMutationType, ErrorType
from .user import AdminUserType


class AdminUserUpdateInputType(InputType):
    __schema__ = gql(
        """
        input UserUpdateInput {
            name: String
            fullName: String
            email: String
            password: String
            isActive: Boolean
            isAdmin: Boolean
            isModerator: Boolean
        }
        """
    )
    __args__ = {
        "fullName": "full_name",
        "isActive": "is_active",
        "isAdmin": "is_admin",
        "isModerator": "is_moderator",
    }


class AdminUserUpdateResultType(ObjectType):
    __schema__ = gql(
        """
        type UserUpdateResult {
            updated: Boolean!
            user: User
            errors: [Error!]
        }
        """
    )
    __requires__ = [AdminUserType, ErrorType]


class AdminUserUpdateMutation(AdminMutationType):
    __schema__ = gql(
        """
        type Mutation {
            userUpdate(user: ID!, input: UserUpdateInput!): UserUpdateResult!
        }
        """
    )
    __requires__ = [AdminUserUpdateInputType, AdminUserUpdateResultType]

    @classmethod
    async def mutate(  # type: ignore
        cls,
        info: GraphQLResolveInfo,
        *,
        user: str,
        input: dict,  # pylint: disable=redefined-builtin
    ):
        input["user"] = user
        cleaned_data, errors = await cls.clean_data(info, input)

        user_obj: Optional[User] = cleaned_data.pop("user", None)
        if errors:
            return {"errors": errors, "updated": False, "user": user_obj}

        if user_obj and cleaned_data:
            updated_user = await cls.update_user(info.context, user_obj, cleaned_data)
            return {"updated": updated_user != user_obj, "user": updated_user}

        return {"updated": False, "user": user_obj}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model(info.context)
        cleaned_data, errors = validate_model(input_model, data)
        cleaned_data, errors = await validate_data(
            cleaned_data,
            {
                "user": [
                    UserExistsValidator(info.context),
                ],
            },
            errors,
        )

        user_obj: Optional[User] = cleaned_data.get("user", None)

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

        return cleaned_data, errors

    @classmethod
    def create_input_model(cls, context: Context) -> Type[BaseModel]:
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

    @classmethod
    async def update_user(
        cls, context: Context, user: User, cleaned_data: dict
    ) -> User:
        user = await user.update(**cleaned_data)
        users_loader.store(context, user)
        return user


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
            raise UserRemoveOwnAdminError()

        return is_admin

    return validate_is_admin
