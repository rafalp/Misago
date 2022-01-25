import pytest

from ..errors import NotAuthenticatedError
from ..validators import IsAuthenticatedValidator


@pytest.mark.asyncio
async def test_validator_doesnt_raise_error_if_user_is_authenticated(
    user_graphql_context,
):
    validator = IsAuthenticatedValidator(user_graphql_context)
    assert await validator({"data": True})


@pytest.mark.asyncio
async def test_validator_raises_not_authenticated_error_when_user_is_not_authenticated(
    graphql_context,
):
    validator = IsAuthenticatedValidator(graphql_context)
    with pytest.raises(NotAuthenticatedError):
        await validator({"data": True})
