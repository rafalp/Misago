from typing import Any, Dict, List, Tuple, Type

from ariadne_graphql_modules import InputType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, EmailStr, create_model

from ...auth import create_user_token
from ...context import Context
from ...users.create import create_user
from ...users.loaders import users_loader
from ...users.models import User
from ...users.validators import (
    EmailIsAvailableValidator,
    UsernameIsAvailableValidator,
    passwordstr,
    usernamestr,
)
from ...validation import ErrorsList, Validator, validate_data, validate_model
from ..mutation import AdminMutationType, ErrorType, MutationType
from ..scalars import GenericScalar
from .hooks.usercreate import (
    UserCreateInput,
    UserCreateInputModel,
    user_create_hook,
    user_create_input_hook,
    user_create_input_model_hook,
)
from .user import AdminUserType, UserType


class UserCreateInputType(InputType):
    __schema__ = gql(
        """
        input UserCreateInput {
            name: String!
            email: String!
            password: String!
            captcha: Generic
        }
        """
    )
    __requires__ = [GenericScalar]


class UserCreateResultType(ObjectType):
    __schema__ = gql(
        """
        type UserCreateResult {
            user: User
            token: String
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, UserType]


class UserCreateMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            userCreate(input: UserCreateInput!): UserCreateResult!
        }
        """
    )
    __requires__ = [UserCreateInputType, UserCreateResultType]

    @classmethod
    async def mutate(
        cls,
        info: GraphQLResolveInfo,
        *,
        input: dict,  # pylint: disable=redefined-builtin
    ):
        cleaned_data, errors = await cls.clean_data(info, input)
        if errors:
            return {"errors": errors}

        user = await user_create_hook.call_action(
            cls.register_user, info.context, cleaned_data
        )
        token = await create_user_token(info.context, user, in_admin=False)

        return {"user": user, "token": token}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = await user_create_input_model_hook.call_action(
            cls.create_input_model, info.context
        )
        cleaned_data, errors = validate_model(input_model, data)

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
                cls.validate_input_data, info.context, validators, cleaned_data, errors
            )

        return cleaned_data, errors

    @classmethod
    async def create_input_model(cls, context: Context) -> UserCreateInputModel:
        return create_model(
            "RegisterInputModel",
            name=(usernamestr(context["settings"]), ...),
            email=(EmailStr, ...),
            password=(passwordstr(context["settings"]), ...),
            captcha=(Any, None),
        )

    @classmethod
    async def validate_input_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: UserCreateInput,
        errors: ErrorsList,
    ) -> Tuple[UserCreateInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    async def register_user(
        cls, context: Context, cleaned_data: UserCreateInput
    ) -> User:
        user = await create_user(
            context,
            cleaned_data["name"],
            cleaned_data["email"],
            password=cleaned_data["password"],
        )
        users_loader.store(context, user)
        return user


class AdminUserCreateInputType(InputType):
    __schema__ = gql(
        """
        input UserCreateInput {
            name: String!
            email: String!
            password: String!
        }
        """
    )


class AdminUserCreateResultType(ObjectType):
    __schema__ = gql(
        """
        type UserCreateResult {
            user: User
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, AdminUserType]


class AdminUserCreateMutation(AdminMutationType):
    __schema__ = gql(
        """
        type Mutation {
            userCreate(input: UserCreateInput!): UserCreateResult!
        }
        """
    )
    __requires__ = [AdminUserCreateInputType, AdminUserCreateResultType]

    @classmethod
    async def mutate(
        cls,
        info: GraphQLResolveInfo,
        *,
        input: dict,  # pylint: disable=redefined-builtin
    ):
        cleaned_data, errors = await cls.clean_data(info, input)
        if errors:
            return {"errors": errors}

        user = await cls.register_user(info.context, cleaned_data)

        return {"user": user}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model(info.context)
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

        return cleaned_data, errors

    @classmethod
    def create_input_model(context: Context) -> Type[BaseModel]:
        return create_model(
            "UserCreateInputModel",
            name=(usernamestr(context["settings"]), ...),
            email=(EmailStr, ...),
            password=(passwordstr(context["settings"]), ...),
        )

    @classmethod
    async def register_user(context: Context, cleaned_data: dict) -> User:
        user = await create_user(
            context,
            cleaned_data["name"],
            cleaned_data["email"],
            password=cleaned_data["password"],
        )
        users_loader.store(context, user)
        return user
