import pytest

from ..cleanarg import clean_id_arg
from ..decorators import handle_invalid_args


@handle_invalid_args
async def clean_arg(arg):
    return clean_id_arg(arg)


@pytest.mark.asyncio
async def test_handle_invalid_args_decorator_does_nothing_for_valid_arg():
    result = await clean_arg("123")
    assert result == 123


@pytest.mark.asyncio
async def test_handle_invalid_args_decorator_returns_null_for_invalid_arg():
    result = await clean_arg("invalid")
    assert result is None
