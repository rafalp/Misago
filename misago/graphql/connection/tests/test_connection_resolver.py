from random import shuffle

import pytest

from ....attachments.models import AttachmentType
from ..connection import Connection
from ..cleanargs import ValidationError

NAMES = "QWERTYUIOPASDFGHJKLZXCVBNM"
LIMIT = 20


@pytest.fixture
async def nodes(db):
    await AttachmentType.query.delete_all()

    nodes_list = []
    for name in NAMES:
        nodes_list.append(await AttachmentType.create(name, []))
    return shuffle(nodes_list)


@pytest.mark.asyncio
async def test_connection_returns_first_five_items_using_default_sorting(
    context, nodes
):
    connection = Connection("name")
    result = await connection.resolve(
        context, AttachmentType.query, {"first": 5}, LIMIT
    )
    names = [edge.node.name for edge in result.edges]
    assert names == ["A", "B", "C", "D", "E"]


@pytest.mark.asyncio
async def test_connection_returns_first_five_items_using_custom_sorting(context, nodes):
    connection = Connection("name")
    result = await connection.resolve(
        context, AttachmentType.query, {"first": 5, "sort_by": "-name"}, LIMIT
    )
    names = [edge.node.name for edge in result.edges]
    assert names == ["Z", "Y", "X", "W", "V"]


@pytest.mark.asyncio
async def test_connection_returns_last_five_items_using_default_sorting(context, nodes):
    connection = Connection("name")
    result = await connection.resolve(context, AttachmentType.query, {"last": 5}, LIMIT)
    names = [edge.node.name for edge in result.edges]
    assert names == ["V", "W", "X", "Y", "Z"]


@pytest.mark.asyncio
async def test_connection_returns_last_five_items_using_custom_sorting(context, nodes):
    connection = Connection("name")
    result = await connection.resolve(
        context, AttachmentType.query, {"last": 5, "sort_by": "-name"}, LIMIT
    )
    names = [edge.node.name for edge in result.edges]
    assert names == ["E", "D", "C", "B", "A"]


@pytest.mark.asyncio
async def test_connection_returns_first_five_items_after_cursor_using_default_sorting(
    context, nodes
):
    connection = Connection("name")
    result = await connection.resolve(
        context, AttachmentType.query, {"first": 5, "after": "E"}, LIMIT
    )
    names = [edge.node.name for edge in result.edges]
    assert names == ["F", "G", "H", "I", "J"]


@pytest.mark.asyncio
async def test_connection_returns_first_five_items_after_cursor_using_custom_sorting(
    context, nodes
):
    connection = Connection("name")
    result = await connection.resolve(
        context,
        AttachmentType.query,
        {"first": 5, "after": "V", "sort_by": "-name"},
        LIMIT,
    )
    names = [edge.node.name for edge in result.edges]
    assert names == ["U", "T", "S", "R", "Q"]


@pytest.mark.asyncio
async def test_connection_returns_last_five_items_before_cursor_using_default_sorting(
    context, nodes
):
    connection = Connection("name")
    result = await connection.resolve(
        context, AttachmentType.query, {"last": 5, "before": "W"}, LIMIT
    )
    names = [edge.node.name for edge in result.edges]
    assert names == ["R", "S", "T", "U", "V"]


@pytest.mark.asyncio
async def test_connection_returns_last_five_items_before_cursor_using_custom_sorting(
    context, nodes
):
    connection = Connection("name")
    result = await connection.resolve(
        context,
        AttachmentType.query,
        {"last": 5, "before": "D", "sort_by": "-name"},
        LIMIT,
    )
    names = [edge.node.name for edge in result.edges]
    assert names == ["I", "H", "G", "F", "E"]


@pytest.mark.asyncio
async def test_connection_sets_next_page_flag(context, nodes):
    connection = Connection("name")

    first_page = await connection.resolve(
        context, AttachmentType.query, {"first": 5}, LIMIT
    )
    assert first_page.has_next_page is True

    middle_page = await connection.resolve(
        context, AttachmentType.query, {"first": 5, "after": "K"}, LIMIT
    )
    assert middle_page.has_next_page is True

    last_page = await connection.resolve(
        context, AttachmentType.query, {"first": 5, "after": "X"}, LIMIT
    )
    assert last_page.has_next_page is False


@pytest.mark.asyncio
async def test_connection_sets_previous_page_flag(context, nodes):
    connection = Connection("name")

    first_page = await connection.resolve(
        context, AttachmentType.query, {"first": 5}, LIMIT
    )
    assert first_page.has_previous_page is False

    middle_page = await connection.resolve(
        context, AttachmentType.query, {"first": 5, "after": "K"}, LIMIT
    )
    assert middle_page.has_previous_page is True

    last_page = await connection.resolve(
        context, AttachmentType.query, {"first": 5, "after": "X"}, LIMIT
    )
    assert last_page.has_previous_page is True


@pytest.mark.asyncio
async def test_connection_sets_first_and_last_cursor(context, nodes):
    connection = Connection("name")

    first_page = await connection.resolve(
        context, AttachmentType.query, {"first": 5}, LIMIT
    )
    assert first_page.start_cursor == "A"
    assert first_page.start_cursor == first_page.edges[0].cursor
    assert first_page.end_cursor == "E"
    assert first_page.end_cursor == first_page.edges[4].cursor

    middle_page = await connection.resolve(
        context, AttachmentType.query, {"first": 5, "after": "K"}, LIMIT
    )
    assert middle_page.start_cursor == "L"
    assert middle_page.start_cursor == middle_page.edges[0].cursor
    assert middle_page.end_cursor == "P"
    assert middle_page.end_cursor == middle_page.edges[4].cursor

    last_page = await connection.resolve(
        context, AttachmentType.query, {"first": 5, "after": "X"}, LIMIT
    )
    assert last_page.start_cursor == "Y"
    assert last_page.start_cursor == last_page.edges[0].cursor
    assert last_page.end_cursor == "Z"
    assert last_page.end_cursor == last_page.edges[1].cursor


@pytest.mark.asyncio
async def test_connection_raises_validation_error_if_after_before_are_combined(
    context, nodes
):
    connection = Connection("name")
    with pytest.raises(ValidationError):
        await connection.resolve(
            context,
            AttachmentType.query,
            {"after": "A", "before": "B"},
            LIMIT,
        )


@pytest.mark.asyncio
async def test_connection_raises_validation_error_if_first_last_are_combined(
    context, nodes
):
    connection = Connection("name")
    with pytest.raises(ValidationError):
        await connection.resolve(
            context,
            AttachmentType.query,
            {"first": 5, "last": 5},
            LIMIT,
        )


@pytest.mark.asyncio
async def test_connection_raises_validation_error_if_first_before(context, nodes):
    connection = Connection("name")
    with pytest.raises(ValidationError):
        await connection.resolve(
            context,
            AttachmentType.query,
            {"first": 5, "before": "B"},
            LIMIT,
        )


@pytest.mark.asyncio
async def test_connection_raises_validation_error_if_last_after_are_combined(
    context, nodes
):
    connection = Connection("name")
    with pytest.raises(ValidationError):
        await connection.resolve(
            context,
            AttachmentType.query,
            {"last": 5, "after": "D"},
            LIMIT,
        )


@pytest.mark.asyncio
async def test_connection_raises_validation_error_for_first_over_limit(context, nodes):
    connection = Connection("name")
    with pytest.raises(ValidationError):
        await connection.resolve(
            context,
            AttachmentType.query,
            {"first": LIMIT + 1},
            LIMIT,
        )


@pytest.mark.asyncio
async def test_connection_raises_validation_error_for_last_over_limit(context, nodes):
    connection = Connection("name")
    with pytest.raises(ValidationError):
        await connection.resolve(
            context,
            AttachmentType.query,
            {"last": LIMIT + 1},
            LIMIT,
        )
