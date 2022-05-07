from typing import Dict, List, Type

from ariadne_graphql_modules import InputType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, EmailStr, constr, create_model

from ...auth import create_user_token
from ...conf.cache import clear_settings_cache
from ...conf.update import update_settings
from ...context import Context
from ...users.create import create_user
from ...users.validators import (
    EmailIsAvailableValidator,
    UsernameIsAvailableValidator,
    passwordstr,
    usernamestr,
)
from ...validation import (
    SiteWizardDisabledError,
    Validator,
    validate_data,
    validate_model,
)
from ..mutation import ErrorType, MutationType
from ..user import UserType


class SiteSetupInputType(InputType):
    __schema__ = gql(
        """
        input SiteSetupInput {
            forumName: String!
            forumIndexThreads: Boolean!
            name: String!
            email: String!
            password: String!
        }
        """
    )
    __args__ = {
        "forumName": "forum_name",
        "forumIndexThreads": "forum_index_threads",
    }


class SiteSetupResultType(ObjectType):
    __schema__ = gql(
        """
        type SiteSetupResult {
            user: User
            token: String
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, UserType]


class SiteSetupMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            siteSetup(input: SiteSetupInput!): SiteSetupResult!
        }
        """
    )
    __requires__ = [SiteSetupInputType, SiteSetupResultType]

    @classmethod
    async def mutate(
        cls,
        info: GraphQLResolveInfo,
        *,
        input: dict,  # pylint: disable=redefined-builtin
    ):
        if not info.context["settings"]["enable_site_wizard"]:
            raise SiteWizardDisabledError()

        cleaned_data, errors = await cls.clean_data(info, input)

        if errors:
            return {"errors": errors}

        await update_settings(
            {
                "enable_site_wizard": False,
                "forum_name": cleaned_data["forum_name"],
                "forum_index_threads": cleaned_data["forum_index_threads"],
            }
        )
        await clear_settings_cache()

        user = await create_user(
            info.context,
            cleaned_data["name"],
            cleaned_data["email"],
            password=cleaned_data["password"],
            is_admin=True,
            is_moderator=True,
        )
        token = await create_user_token(info.context, user, in_admin=False)

        return {"user": user, "token": token}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model(info.context)
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
            cleaned_data, errors = await validate_data(cleaned_data, validators, errors)

        return cleaned_data, errors

    @classmethod
    def create_input_model(cls, context: Context) -> Type[BaseModel]:
        return create_model(
            "SiteSetupInputModel",
            forum_name=(
                constr(strip_whitespace=True, min_length=1, max_length=150),
                ...,
            ),
            forum_index_threads=(bool, ...),
            name=(usernamestr(context["settings"]), ...),
            email=(EmailStr, ...),
            password=(passwordstr(context["settings"]), ...),
        )
