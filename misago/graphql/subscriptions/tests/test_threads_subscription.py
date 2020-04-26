import json
from dataclasses import replace

import pytest

from ....pubsub.threads import THREADS_CHANNEL, serialize_message
from ..threads import threads_resolver, threads_source


@pytest.mark.asyncio
async def test_threads_updates_source_yields_thread(mock_subscribe, thread):
    message = serialize_message(thread)
    mock_subscribe(THREADS_CHANNEL, message)
    events = [event async for event in threads_source()]
    assert events == [json.loads(message)]


@pytest.mark.asyncio
async def test_threads_updates_source_yields_subscribed_category_thread(
    mock_subscribe, thread, category
):
    message = serialize_message(thread)
    mock_subscribe(THREADS_CHANNEL, message)
    events = [event async for event in threads_source(category=category.id)]
    assert events == [json.loads(message)]


@pytest.mark.asyncio
async def test_threads_updates_source_yields_subscribed_category_child_thread(
    mock_subscribe, thread, category, child_category
):
    thread = replace(thread, category_id=child_category.id)
    message = serialize_message(thread)
    mock_subscribe(THREADS_CHANNEL, message)
    events = [event async for event in threads_source(category=category.id)]
    assert events == [json.loads(message)]


@pytest.mark.asyncio
async def test_threads_updates_source_skips_subscribed_category_parent_thread(
    mock_subscribe, thread, child_category
):
    message = serialize_message(thread)
    mock_subscribe(THREADS_CHANNEL, message)
    events = [event async for event in threads_source(category=child_category.id)]
    assert events == []


@pytest.mark.asyncio
async def test_threads_updates_source_skips_subscribed_category_sibling_thread(
    mock_subscribe, thread, category, sibling_category
):
    thread = replace(thread, category_id=sibling_category.id)
    message = serialize_message(thread)
    mock_subscribe(THREADS_CHANNEL, message)
    events = [event async for event in threads_source(category=category.id)]
    assert events == []


@pytest.mark.asyncio
async def test_threads_updates_source_skips_removed_category_thread(
    mock_subscribe, thread, category
):
    thread = replace(thread, category_id=category.id * 20)
    message = serialize_message(thread)
    mock_subscribe(THREADS_CHANNEL, message)
    events = [event async for event in threads_source()]
    assert events == []


@pytest.mark.asyncio
async def test_threads_updates_source_skips_invalid_category_subscription(
    mock_subscribe, thread, category
):
    message = serialize_message(thread)
    mock_subscribe(THREADS_CHANNEL, message)
    events = [event async for event in threads_source(category=category.id * 20)]
    assert events == []


def test_threads_updates_resolver_resolves_thread_id_from_event():
    assert threads_resolver({"id": 123}) == 123
