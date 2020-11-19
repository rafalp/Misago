import pytest

from ..create import create_user
from ..suggestions import find_users_suggestions


@pytest.mark.asyncio
async def test_suggestions_include_user_with_slug_exact_match(db):
    user = await create_user("User", "johndoe@example.com")
    results = await find_users_suggestions("user")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_suggestions_include_user_with_slug_prefix_match(db):
    user = await create_user("TestUser", "johndoe@example.com")
    results = await find_users_suggestions("test")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_suggestions_slug_search_is_case_insensitive(db):
    user = await create_user("User", "johndoe@example.com", full_name="John Doe")
    results = await find_users_suggestions("USER")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_suggestions_include_user_with_full_name_exact_match(db):
    user = await create_user("User", "johndoe@example.com", full_name="John Doe")
    results = await find_users_suggestions("John Doe")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_suggestions_full_name_search_is_case_insensitive(db):
    user = await create_user("User", "johndoe@example.com", full_name="John Doe")
    results = await find_users_suggestions("JOHN DOE")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_suggestions_include_user_with_full_name_prefix_match(db):
    user = await create_user("User", "johndoe@example.com", full_name="John Doe")
    results = await find_users_suggestions("John")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_suggestions_display_exact_slug_matches_first(db):
    suggestion = await create_user("JohnDoe", "user1@example.com")
    exact_match = await create_user("John", "user2@example.com")

    results = await find_users_suggestions("John")
    assert len(results) == 2
    assert results[0].id == exact_match.id
    assert results[1].id == suggestion.id


@pytest.mark.asyncio
async def test_suggestions_display_exact_full_name_matches_first(db):
    suggestion = await create_user("a", "user1@example.com", full_name="John Doe")
    exact_match = await create_user("b", "user2@example.com", full_name="John")

    results = await find_users_suggestions("John")
    assert len(results) == 2
    assert results[0].id == exact_match.id
    assert results[1].id == suggestion.id


@pytest.mark.asyncio
async def test_suggestions_search_escapes_search_string(db):
    await create_user("bob", "user1@example.com", full_name="John Doe")
    exact_match = await create_user("John", "user2@example.com", full_name=r"%doe")

    results = await find_users_suggestions(r"%doe")
    assert len(results) == 1
    assert results[0].id == exact_match.id
