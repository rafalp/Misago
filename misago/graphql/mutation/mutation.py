from inspect import isawaitable
from typing import Union

from ariadne_graphql_modules import MutationType

from ...validation import VALIDATION_ERRORS, ErrorDict, ErrorsList, get_error_dict
from ..errors import AuthenticationGraphQLError, ForbiddenGraphQLError

ERRORS = "errors"


class Mutation(MutationType):
    __abstract__ = True

    @classmethod
    async def resolve_mutation(cls, _, info, **arguments):
        try:
            result = await cls.mutate(info, **arguments)
            if isawaitable(result):
                result = await result
        except VALIDATION_ERRORS as error:
            result = {ERRORS: [error]}

        if result.get(ERRORS):
            result[ERRORS] = ErrorsList([format_error(e) for e in result[ERRORS]])

        return result

    @classmethod
    async def mutate(cls, info, **arguments):
        raise NotImplementedError(
            "Mutation subclassess should override 'mutate' class method"
        )


def format_error(error: Union[ErrorDict, Exception]) -> ErrorDict:
    if isinstance(error, Exception):
        return get_error_dict(error)
    return error


class AdminMutation(Mutation):
    __abstract__ = True

    @classmethod
    async def resolve_mutation(cls, _, info, **arguments):
        user = info.context["user"]
        if not user:
            raise AuthenticationGraphQLError()
        if not user.is_admin:
            raise ForbiddenGraphQLError()

        return await super().resolve_mutation(_, info, **arguments)
