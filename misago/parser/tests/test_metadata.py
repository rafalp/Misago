from ..metadata import create_ast_metadata


def test_create_ast_metadata_creates_metadata_for_empty_ast(parser_context):
    metadata = create_ast_metadata(parser_context, [])
    assert metadata["usernames"] == set()
    assert metadata["users"] == {}


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
                    {"type": "text", "text": f"Hello "},
                    {"type": "mention", "username": user.username},
                    {"type": "text", "text": f"!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": f"See "},
                    {"type": "mention", "username": other_user.username},
                    {"type": "text", "text": f"."},
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
                    {"type": "text", "text": f"Hello "},
                    {"type": "mention", "username": user.username},
                    {"type": "text", "text": f"!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": f"See "},
                    {"type": "mention", "username": "Doesnt_Exist"},
                    {"type": "text", "text": f"."},
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
                    {"type": "text", "text": f"Hello "},
                    {"type": "mention", "username": user.username},
                    {"type": "text", "text": f"!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": f"See "},
                    {"type": "mention", "username": user.username},
                    {"type": "text", "text": f"."},
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
                    {"type": "text", "text": f"Hello "},
                    {"type": "mention", "username": user.username.upper()},
                    {"type": "text", "text": f"!"},
                ],
            },
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": f"See "},
                    {"type": "mention", "username": user.username.lower()},
                    {"type": "text", "text": f"."},
                ],
            },
            {"type": "thematic-break"},
        ],
    )
    assert metadata["usernames"] == set([user.slug])
    assert metadata["users"] == {user.slug: user}
