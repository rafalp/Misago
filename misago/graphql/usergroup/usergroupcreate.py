from typing import Dict, List, Optional

from ariadne_graphql_modules import InputType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, constr

from ...users.models import UserGroup
from ...validation import Validator, validate_data, validate_model
from ..mutation import AdminMutationType, ErrorType
from .usergroup import AdminUserGroupType


class AdminUserGroupCreateInputType(InputType):
    __schema__ = gql(
        """
        input UserGroupCreateInput {
            name: String!
            title: String
            cssSuffix: String
            isHidden: Boolean
            isModerator: Boolean
            isAdmin: Boolean
        }
        """
    )
    __args__ = {
        "title": "title",
        "cssSuffix": "css_suffix",
        "isHidden": "is_hidden",
        "isModerator": "is_moderator",
        "isAdmin": "is_admin",
    }


class AdminUserGroupCreateResultType(ObjectType):
    __schema__ = gql(
        """
        type UserGroupCreateResult {
            group: UserGroup
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, AdminUserGroupType]


class AdminUserGroupCreateMutation(AdminMutationType):
    __schema__ = gql(
        """
        type Mutation {
            userGroupCreate(input: UserGroupCreateInput!): UserGroupCreateResult!
        }
        """
    )
    __requires__ = [AdminUserGroupCreateInputType, AdminUserGroupCreateResultType]

    @classmethod
    async def mutate(  # type: ignore
        cls,
        info: GraphQLResolveInfo,
        *,
        input: dict,  # pylint: disable=redefined-builtin
    ):
        cleaned_data, errors = await cls.clean_data(info, input)
        if errors:
            return {"errors": errors}

        group = await cls.create_group(cleaned_data)

        return {"group": group}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        cleaned_data, errors = validate_model(UserGroupCreateInputModel, data)

        if cleaned_data:
            validators: Dict[str, List[Validator]] = {}
            cleaned_data, errors = await validate_data(cleaned_data, validators, errors)

        return cleaned_data, errors

    @classmethod
    async def create_group(cls, cleaned_data: dict) -> UserGroup:
        return await UserGroup.create(
            cleaned_data["name"],
            title=cleaned_data["title"],
            css_suffix=cleaned_data["css_suffix"],
            is_hidden=cleaned_data["is_hidden"],
            is_moderator=cleaned_data["is_moderator"],
            is_admin=cleaned_data["is_admin"],
        )


class UserGroupCreateInputModel(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=255, regex=r"\w")
    title: Optional[constr(strip_whitespace=True, min_length=0, max_length=255)] = None
    css_suffix: Optional[
        constr(strip_whitespace=True, min_length=0, max_length=255, regex=r"(?!\s)*")
    ] = None
    is_hidden: bool = False
    is_moderator: bool = False
    is_admin: bool = False
