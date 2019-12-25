import pytest

from ...errors import UsernameNotAvailableError
from ..validators import UsernameIsAvailableValidator


@pytest.mark.asyncio
async def test_validator_allows_username_if_its_not_used_by_other_user(db):
    validator = UsernameIsAvailableValidator()
    assert await validator("TestUsername") == "TestUsername"


@pytest.mark.asyncio
async def test_validator_allows_username_if_its_used_by_excluded_user(user):
    validator = UsernameIsAvailableValidator(user.id)
    assert await validator(user.name) == user.name


@pytest.mark.asyncio
async def test_validator_raises_error_if_username_is_not_available(user):
    validator = UsernameIsAvailableValidator()
    with pytest.raises(UsernameNotAvailableError):
        await validator(user.name)


@pytest.mark.asyncio
async def test_validator_raises_error_if_username_is_used_by_non_excluded_user(
    user, other_user
):
    validator = UsernameIsAvailableValidator(user.id)
    with pytest.raises(UsernameNotAvailableError):
        await validator(other_user.name)
