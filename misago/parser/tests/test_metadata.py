from ..metadata import create_ast_metadata


def test_create_ast_metadata_creates_metadata_for_empty_ast(parser_context):
    metadata = create_ast_metadata(parser_context, [])
    assert metadata["outbound-links"] == set()
    assert metadata["usernames"] == set()
    assert metadata["users"] == {}


def test_create_ast_metadata_creates_metadata_for_ast_with_attachments(parser_context):
    metadata = create_ast_metadata(
        parser_context,
        [
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "Hello "},
                    {"type": "attachment", "name": "file.png", "id": 123},
                    {"type": "text", "text": "!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": "See "},
                    {"type": "attachment", "name": "image.png", "id": 41},
                    {"type": "text", "text": "."},
                ],
            },
            {"type": "thematic-break"},
        ],
    )
    assert metadata["attachments"] == set([41, 123])


def test_create_ast_metadata_creates_metadata_for_ast_with_mentions(
    parser_context, user, other_user
):
    metadata = create_ast_metadata(
        parser_context,
        [
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "Hello "},
                    {"type": "mention", "username": user.username},
                    {"type": "text", "text": "!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": "See "},
                    {"type": "mention", "username": other_user.username},
                    {"type": "text", "text": "."},
                ],
            },
            {"type": "thematic-break"},
        ],
    )
    assert metadata["usernames"] == set([user.slug, other_user.slug])
    assert metadata["users"] == {
        user.slug: user,
        other_user.slug: other_user,
    }


def test_create_ast_metadata_handles_nonexisting_users_mentions(parser_context, user):
    metadata = create_ast_metadata(
        parser_context,
        [
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "Hello "},
                    {"type": "mention", "username": user.username},
                    {"type": "text", "text": "!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": f"See "},
                    {"type": "mention", "username": "Doesnt_Exist"},
                    {"type": "text", "text": "."},
                ],
            },
            {"type": "thematic-break"},
        ],
    )
    assert metadata["usernames"] == set([user.slug, "doesnt-exist"])
    assert metadata["users"] == {user.slug: user}


def test_create_ast_metadata_handles_repeated_users_mentions(parser_context, user):
    metadata = create_ast_metadata(
        parser_context,
        [
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "Hello "},
                    {"type": "mention", "username": user.username},
                    {"type": "text", "text": "!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": "See "},
                    {"type": "mention", "username": user.username},
                    {"type": "text", "text": "."},
                ],
            },
            {"type": "thematic-break"},
        ],
    )
    assert metadata["usernames"] == set([user.slug])
    assert metadata["users"] == {user.slug: user}


def test_create_ast_metadata_normalizes_mentioned_users_names(parser_context, user):
    metadata = create_ast_metadata(
        parser_context,
        [
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "Hello "},
                    {"type": "mention", "username": user.username.upper()},
                    {"type": "text", "text": "!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": f"See "},
                    {"type": "mention", "username": user.username.lower()},
                    {"type": "text", "text": "."},
                ],
            },
            {"type": "thematic-break"},
        ],
    )
    assert metadata["usernames"] == set([user.slug])
    assert metadata["users"] == {user.slug: user}


def test_create_ast_metadata_includes_an_outbound_link(parser_context):
    metadata = create_ast_metadata(
        parser_context,
        [
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "Hello!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": "See "},
                    {
                        "type": "url",
                        "href": "my-website.com",
                        "children": [{"type": "text", "text": "my homepage"}],
                    },
                    {"type": "text", "text": "!"},
                ],
            },
            {"type": "thematic-break"},
        ],
    )
    assert metadata["outbound-links"] == set(["my-website.com"])


def test_create_ast_metadata_outbound_links_excludes_inbound_link(parser_context):
    metadata = create_ast_metadata(
        parser_context,
        [
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "Hello!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": "See "},
                    {
                        "type": "url",
                        "href": "example.org/t/123/",
                        "children": [{"type": "text", "text": "this thread"}],
                    },
                    {"type": "text", "text": "!"},
                ],
            },
            {"type": "thematic-break"},
        ],
    )
    assert metadata["outbound-links"] == set()


def test_create_ast_metadata_visits_lists_items(parser_context, user):
    metadata = create_ast_metadata(
        parser_context,
        [
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "Hello!"},
                ],
            },
            {
                "type": "list",
                "ordered": False,
                "sign": "+",
                "items": [
                    {
                        "type": "list-item",
                        "children": [
                            {
                                "type": "text",
                                "text": "Lorem ",
                            },
                            {"type": "mention", "username": user.username},
                        ],
                        "lists": [],
                    },
                    {
                        "type": "list-item",
                        "children": [
                            {
                                "type": "text",
                                "text": "Ipsum",
                            },
                        ],
                        "lists": [],
                    },
                ],
            },
        ],
    )
    assert metadata["usernames"] == set([user.slug])
    assert metadata["users"] == {user.slug: user}


def test_create_ast_metadata_visits_nested_lists_items(parser_context, user):
    metadata = create_ast_metadata(
        parser_context,
        [
            {
                "type": "heading",
                "level": 1,
                "children": [
                    {"type": "text", "text": "Hello!"},
                ],
            },
            {
                "type": "list",
                "ordered": False,
                "sign": "-",
                "items": [
                    {
                        "type": "list-item",
                        "children": [
                            {
                                "type": "text",
                                "text": "Lorem ",
                            },
                        ],
                        "lists": [
                            {
                                "type": "list",
                                "ordered": True,
                                "sign": None,
                                "items": [
                                    {
                                        "type": "list-item",
                                        "children": [
                                            {
                                                "type": "text",
                                                "text": "Ipsum",
                                            },
                                            {
                                                "type": "mention",
                                                "username": user.username,
                                            },
                                        ],
                                        "lists": [],
                                    },
                                ],
                            }
                        ],
                    },
                ],
            },
        ],
    )
    assert metadata["usernames"] == set([user.slug])
    assert metadata["users"] == {user.slug: user}
