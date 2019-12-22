import pytest

from ...errors import NotAuthorizedError
from ..validators import UserIsAuthorizedRootValidator


@pytest.mark.asyncio
async def test_validator_doesnt_raise_error_if_user_is_authorized(user_graphql_context):
    validator = UserIsAuthorizedRootValidator(user_graphql_context)
    assert await validator({"data": True})


@pytest.mark.asyncio
async def test_validator_raises_not_authorized_error_when_user_is_not_authorized(
    graphql_context,
):
    validator = UserIsAuthorizedRootValidator(graphql_context)
    with pytest.raises(NotAuthorizedError):
        await validator({"data": True})
