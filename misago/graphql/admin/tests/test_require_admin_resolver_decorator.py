import pytest

from ....errors import NotAdminError
from ..requireadmin import require_admin


@require_admin
def admin_resolver(*args, **kwargs):
    pass


@pytest.mark.asyncio
async def test_no_error_is_raised_when_resolver_is_called_with_admin_auth(
    admin_graphql_info,
):
    await admin_resolver(None, admin_graphql_info)


@pytest.mark.asyncio
async def test_not_admin_error_is_raised_when_resolver_is_called_without_admin_auth(
    user_graphql_info,
):
    with pytest.raises(NotAdminError):
        await admin_resolver(None, user_graphql_info)


@pytest.mark.asyncio
async def test_not_admin_error_is_raised_when_resolver_is_called_without_any_auth(
    graphql_info,
):
    with pytest.raises(NotAdminError):
        await admin_resolver(None, graphql_info)
