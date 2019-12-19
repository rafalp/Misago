import pytest

from ...errors import EmailIsNotAvailableError
from ..validators import validate_email_is_available


@pytest.mark.asyncio
async def test_validator_allows_email_if_its_not_used_by_other_user(db):
    validator = validate_email_is_available()
    await validator("new@example.com")


@pytest.mark.asyncio
async def test_validator_allows_email_if_its_used_by_excluded_user(user):
    validator = validate_email_is_available(user.id)
    await validator(user.email)


@pytest.mark.asyncio
async def test_validator_raises_error_if_email_is_not_available(user):
    validator = validate_email_is_available()
    with pytest.raises(EmailIsNotAvailableError):
        await validator(user.email)


@pytest.mark.asyncio
async def test_validator_raises_error_if_email_is_used_by_non_excluded_user(
    user, other_user
):
    validator = validate_email_is_available(user.id)
    with pytest.raises(EmailIsNotAvailableError):
        await validator(other_user.email)
