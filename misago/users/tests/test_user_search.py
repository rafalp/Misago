import pytest

from ..create import create_user
from ..search import search_users


@pytest.mark.asyncio
async def test_search_returns_user_with_slug_exact_match(db):
    user = await create_user("User", "johndoe@example.com")
    results = await search_users("user")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_search_returns_user_with_slug_prefix_match(db):
    user = await create_user("TestUser", "johndoe@example.com")
    results = await search_users("test")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_search_by_slug_is_case_insensitive(db):
    user = await create_user("User", "johndoe@example.com", full_name="John Doe")
    results = await search_users("USER")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_search_returns_user_with_full_name_exact_match(db):
    user = await create_user("User", "johndoe@example.com", full_name="John Doe")
    results = await search_users("John Doe")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_search_by_name_is_case_insensitive(db):
    user = await create_user("User", "johndoe@example.com", full_name="John Doe")
    results = await search_users("JOHN DOE")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_search_returns_user_with_full_name_prefix_match(db):
    user = await create_user("User", "johndoe@example.com", full_name="John Doe")
    results = await search_users("John")
    assert len(results) == 1
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_search_returns_exact_slug_matches_first(db):
    suggestion = await create_user("JohnDoe", "user1@example.com")
    exact_match = await create_user("John", "user2@example.com")

    results = await search_users("John")
    assert len(results) == 2
    assert results[0].id == exact_match.id
    assert results[1].id == suggestion.id


@pytest.mark.asyncio
async def test_search_returns_exact_full_name_matches_first(db):
    suggestion = await create_user("a", "user1@example.com", full_name="John Doe")
    exact_match = await create_user("b", "user2@example.com", full_name="John")

    results = await search_users("John")
    assert len(results) == 2
    assert results[0].id == exact_match.id
    assert results[1].id == suggestion.id


@pytest.mark.asyncio
async def test_search_escapes_searched_query(db):
    await create_user("bob", "user1@example.com", full_name="John Doe")
    exact_match = await create_user("John", "user2@example.com", full_name=r"%doe")

    results = await search_users(r"%doe")
    assert len(results) == 1
    assert results[0].id == exact_match.id


@pytest.mark.asyncio
async def test_search_returns_empty_list_when_limit_is_less_than_1(db):
    await create_user("bob", "user1@example.com", full_name="John Doe")

    results = await search_users("bob", limit=0)
    assert results == []
