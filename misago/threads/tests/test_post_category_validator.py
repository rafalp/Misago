from asyncio import Future
from unittest.mock import Mock

import pytest

from ..validators import PostCategoryValidator


@pytest.mark.asyncio
async def test_post_category_validator_calls_given_validator_against_post_category(
    post, category, graphql_context
):
    future = Future()
    future.set_result(category)
    category_validator = Mock(return_value=future)
    validator = PostCategoryValidator(graphql_context, category_validator)
    await validator(post, "errors", "field")
    category_validator.assert_called_once_with(category, "errors", "field")


@pytest.mark.asyncio
async def test_post_category_validator_wrapped_validator_can_be_retrieved(
    graphql_context,
):
    category_validator = Mock()
    validator = PostCategoryValidator(graphql_context, category_validator)
    assert validator.category_validator is category_validator
