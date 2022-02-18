import pytest

from ..errors import NotAuthenticatedError
from ..validators import IsAuthenticatedValidator


@pytest.mark.asyncio
async def test_validator_doesnt_raise_error_if_user_is_authenticated(user_context):
    validator = IsAuthenticatedValidator(user_context)
    assert await validator({"data": True})


@pytest.mark.asyncio
async def test_validator_raises_not_authenticated_error_when_user_is_not_authenticated(
    context,
):
    validator = IsAuthenticatedValidator(context)
    with pytest.raises(NotAuthenticatedError):
        await validator({"data": True})
