import pytest

from ..register import resolve_register


@pytest.mark.asyncio
async def test_registration_mutation_creates_new_user_account(graphql_info):
    await resolve_register(
        None,
        graphql_info,
        input={
            "name": "John",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )
