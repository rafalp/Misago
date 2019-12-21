from asyncio import Future
from unittest.mock import Mock

import pytest

from ..validators import PostCategoryValidator


@pytest.mark.asyncio
async def test_post_category_validator_calls_given_validator_against_post_category(
    post, category
):
    future = Future()
    future.set_result(category)
    category_validator = Mock(return_value=future)
    validator = PostCategoryValidator({}, category_validator)
    await validator(post, None)
    category_validator.assert_called_once_with(category, None)


@pytest.mark.asyncio
async def test_post_category_validator_wrapped_validator_can_be_retrieved():
    category_validator = Mock()
    validator = PostCategoryValidator({}, category_validator)
    assert validator.category_validator is category_validator
