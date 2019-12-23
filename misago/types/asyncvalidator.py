from typing import Any, Protocol

from ..errors import ErrorsList


class AsyncValidator(Protocol):
    async def __call__(self, value: Any, errors: ErrorsList, field_name: str) -> Any:
        ...
