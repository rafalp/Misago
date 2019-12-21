from asyncio import Future
from unittest.mock import Mock

import pytest

from ..validators import ThreadCategoryValidator


@pytest.mark.asyncio
async def test_thread_category_validator_calls_given_validator_against_thread_category(
    thread, category
):
    future = Future()
    future.set_result(category)
    category_validator = Mock(return_value=future)
    validator = ThreadCategoryValidator({}, category_validator)
    await validator(thread, None)
    category_validator.assert_called_once_with(category, None)


@pytest.mark.asyncio
async def test_thread_category_validator_wrapped_validator_can_be_retrieved():
    category_validator = Mock()
    validator = ThreadCategoryValidator({}, category_validator)
    assert validator.category_validator is category_validator
