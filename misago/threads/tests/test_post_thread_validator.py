from asyncio import Future
from unittest.mock import Mock

import pytest

from ..validators import PostThreadValidator


@pytest.mark.asyncio
async def test_post_thread_validator_calls_given_validator_against_post_thread(
    post, thread
):
    future = Future()
    future.set_result(thread)
    thread_validator = Mock(return_value=future)
    validator = PostThreadValidator({}, thread_validator)
    await validator(post, "errors", "field")
    thread_validator.assert_called_once_with(thread, "errors", "field")


@pytest.mark.asyncio
async def test_post_thread_validator_wrapped_validator_can_be_retrieved():
    thread_validator = Mock()
    validator = PostThreadValidator({}, thread_validator)
    assert validator.thread_validator is thread_validator
