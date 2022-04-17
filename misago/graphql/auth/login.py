from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...auth import authenticate_user, create_user_token
from ...auth.errors import InvalidCredentialsError, NotAdminError
from ...validation import AllFieldsAreRequiredError
from ..mutation import ErrorType, MutationType
from ..users import UserType


class LoginMutationResult(ObjectType):
    __schema__ = gql(
        """
        type LoginMutationResult {
            user: User
            token: String
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, UserType]


class LoginMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            login(username: String!, password: String!): LoginMutationResult!
        }
        """
    )
    __requires__ = [LoginMutationResult]

    @staticmethod
    async def mutate(info: GraphQLResolveInfo, *, username: str, password: str) -> dict:
        username = str(username or "").strip()
        password = str(password or "")

        if not username or not password:
            raise AllFieldsAreRequiredError()

        user = await authenticate_user(info.context, username, password, in_admin=False)

        if not user:
            raise InvalidCredentialsError()

        token = await create_user_token(info.context, user, in_admin=False)
        return {"user": user, "token": token}


class AdminLoginMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            login(username: String!, password: String!): LoginMutationResult!
        }
        """
    )
    __requires__ = [LoginMutationResult]

    @staticmethod
    async def mutate(info: GraphQLResolveInfo, *, username: str, password: str) -> dict:
        username = str(username or "").strip()
        password = str(password or "")

        if not username or not password:
            raise AllFieldsAreRequiredError()

        user = await authenticate_user(info.context, username, password, in_admin=True)

        if not user:
            raise InvalidCredentialsError()
        if not user.is_admin:
            raise NotAdminError()

        token = await create_user_token(info.context, user, in_admin=True)
        return {"user": user, "token": token}
