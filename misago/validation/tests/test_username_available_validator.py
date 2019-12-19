import pytest

from ...errors import UsernameIsNotAvailableError
from ..validators import validate_username_is_available


@pytest.mark.asyncio
async def test_validator_allows_username_if_its_not_used_by_other_user(db):
    validator = validate_username_is_available()
    assert await validator("TestUsername") == "TestUsername"


@pytest.mark.asyncio
async def test_validator_allows_username_if_its_used_by_excluded_user(user):
    validator = validate_username_is_available(user.id)
    assert await validator(user.name) == user.name


@pytest.mark.asyncio
async def test_validator_raises_error_if_username_is_not_available(user):
    validator = validate_username_is_available()
    with pytest.raises(UsernameIsNotAvailableError):
        await validator(user.name)


@pytest.mark.asyncio
async def test_validator_raises_error_if_username_is_used_by_non_excluded_user(
    user, other_user
):
    validator = validate_username_is_available(user.id)
    with pytest.raises(UsernameIsNotAvailableError):
        await validator(other_user.name)
