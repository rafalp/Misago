from typing import Any, Awaitable, Callable, Union

from ..errors import ErrorsList

Validator = Callable[[Any, ErrorsList, str], Union[Awaitable[Any], Any]]
