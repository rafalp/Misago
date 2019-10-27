from typing import List, Tuple

from asgiref.sync import sync_to_async
from passlib.utils.handlers import GenericHandler


class PasswordHasher:
    _hashers: List[GenericHandler]

    def __init__(self, *hashers: Tuple[GenericHandler]):
        self._hashers = list(hashers)

    def add_hasher(self, hasher: GenericHandler):
        self._hashers.insert(0, hasher)

    def add_deprecated_hasher(self, hasher: GenericHandler):
        self._hashers.append(hasher)

    async def hash_password(self, password: str) -> str:
        return await _hash_password(self._hashers[0], password)

    async def verify_password(self, password: str, password_hash: str) -> bool:
        for hasher in self._hashers:
            if await _verify_password(hasher, password, password_hash):
                return True
        return False

    async def is_password_outdated(self, password: str, password_hash: str) -> bool:
        return await _verify_password(self._hashers[0], password, password_hash)


@sync_to_async
def _hash_password(hasher: GenericHandler, password: str) -> str:
    return hasher.hash(password)


@sync_to_async
def _verify_password(hasher: GenericHandler, password: str, password_hash: str) -> bool:
    return hasher.verify(password, password_hash)
