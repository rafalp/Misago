import pytest
from passlib.hash import pbkdf2_sha256, plaintext

from . import password_hasher
from .hasher import PasswordHasher

PASSWORD = "p4ssw0rd"


@pytest.mark.asyncio
async def test_raw_password_can_be_hashed():
    assert await password_hasher.hash_password(PASSWORD)


@pytest.mark.asyncio
async def test_valid_password_hash_is_verified():
    password_hash = await password_hasher.hash_password(PASSWORD)
    assert await password_hasher.check_password(PASSWORD, password_hash)


@pytest.mark.asyncio
async def test_invalid_password_hash_fails_verification():
    password_hash = await password_hasher.hash_password(PASSWORD)
    assert not await password_hasher.check_password("invalid", password_hash)


@pytest.mark.asyncio
async def test_new_default_password_hasher_can_be_added_after_initialization():
    hasher = PasswordHasher([plaintext])
    hasher.add_hasher(pbkdf2_sha256)

    password_hash = await hasher.hash_password(PASSWORD)
    assert password_hash.startswith("$pbkdf2-sha256$")


@pytest.mark.asyncio
async def test_new_deprecated_password_hasher_can_be_added_after_initialization():
    hasher = PasswordHasher([pbkdf2_sha256])
    hasher.add_deprecated_hasher(plaintext)

    password_hash = await hasher.hash_password(PASSWORD)
    assert password_hash.startswith("$pbkdf2-sha256$")


@pytest.mark.asyncio
async def test_deprecated_password_hash_is_verified():
    hasher = PasswordHasher([plaintext])
    password_hash = await hasher.hash_password(PASSWORD)

    hasher.add_hasher(pbkdf2_sha256)
    assert await password_hasher.check_password(PASSWORD, password_hash)


@pytest.mark.asyncio
async def test_deprecated_password_hash_is_detected_as_outdated():
    hasher = PasswordHasher([plaintext])
    password_hash = await hasher.hash_password(PASSWORD)
    hasher.add_hasher(pbkdf2_sha256)
    assert await password_hasher.is_password_outdated(PASSWORD, password_hash)


@pytest.mark.asyncio
async def test_password_hash_is_detected_as_up_to_date():
    hasher = PasswordHasher([pbkdf2_sha256])
    password_hash = await hasher.hash_password(PASSWORD)
    hasher.add_hasher(plaintext)
    assert not await password_hasher.is_password_outdated(PASSWORD, password_hash)
